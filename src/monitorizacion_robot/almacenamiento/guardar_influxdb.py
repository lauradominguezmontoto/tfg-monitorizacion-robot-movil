from datetime import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def crear_punto(measurement, registro, fecha_hora):

    punto = Point(measurement)

    punto.tag("id_dispositivo", str(registro["id_dispositivo"]))
    punto.tag("modo_datos", str(registro["modo_datos"]))
    punto.tag("modo_funcionamiento", str(registro["modo_funcionamiento"]))
    punto.tag("conexion_ok", str(registro["conexion_ok"]))
    punto.tag("hay_anomalia", str(registro["hay_anomalia"]))
    punto.time(fecha_hora)

    return punto


def obtener_anomalias_variable(registro, variable):

    anomalias_variable = []

    for anomalia in registro["anomalias_simples"]:

        if variable in anomalia:
            anomalias_variable.append(anomalia)

        elif variable == "distancia_frontal" and anomalia == "cambio_brusco_distancia":
            anomalias_variable.append(anomalia)

    if anomalias_variable:
        return ", ".join(anomalias_variable)

    return "NINGUNA"


def anadir_datos_variable(punto, registro, variable, sufijo = ""):

    valor = registro["sensores"][variable]
    estado = registro["estados"][variable]

    punto.field("disponible" + sufijo, valor is not None)

    if valor is not None:
        punto.field("valor" + sufijo, float(valor))

    punto.tag("estado" + sufijo, str(estado))
    punto.tag("anomalia_simple" + sufijo, obtener_anomalias_variable(registro, variable))


def enviar_registro_influx(registro, config):

    influx = config["influxdb"]

    cliente = InfluxDBClient(url = influx["url"], token = influx["token"], org = influx["org"])
    escribir_api = cliente.write_api(write_options = SYNCHRONOUS)

    variables = ["temperatura", "humedad", "luz", "gas", "bateria", "corriente", "pitch", "roll", "distancia_frontal"]

    variables_anomalias = {
        "posible_incidente_gas": ["temperatura", "gas"],
        "posible_atasco": ["distancia_frontal", "corriente", "pitch", "roll"]
    }

    fecha_hora = datetime.strptime(registro["fecha_hora"], "%d/%m/%Y %H:%M:%S").astimezone()

    puntos = []


    # Telemetría

    for variable in variables:

        punto = crear_punto(influx["measurement_telemetria"], registro, fecha_hora)
        punto.tag("variable", variable)

        anadir_datos_variable(punto, registro, variable)

        puntos.append(punto)


    # Anomalías complejas

    for anomalia_compleja in registro["anomalias_complejas"]:

        if anomalia_compleja not in variables_anomalias:
            continue

        evento = crear_punto(influx["measurement_eventos"], registro, fecha_hora)
        evento.tag("anomalia_compleja", anomalia_compleja)

        for variable in variables_anomalias[anomalia_compleja]:
            anadir_datos_variable(evento, registro, variable, "_" + variable)

        puntos.append(evento)


    # Eventos

    for nombre_evento in registro["eventos"]:

        evento = crear_punto(influx["measurement_eventos"], registro, fecha_hora)

        evento.tag("evento", nombre_evento)
        evento.field("evento_detectado", True)

        if nombre_evento == "posible_caida":

            for variable in ["pitch", "roll"]:
                anadir_datos_variable(evento, registro, variable, "_" + variable)

        puntos.append(evento)


    try:
        escribir_api.write(bucket = influx["bucket"], org = influx["org"], record = puntos)
        return True

    except Exception as error:
        print("No se pudo enviar el registro a InfluxDB")
        print(error)
        return False

    finally:
        cliente.close()