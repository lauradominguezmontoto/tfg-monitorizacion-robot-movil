import json
import time

from .adquisicion import simulador_datos as sd, recepcion_mqtt as rm
from .procesado import procesado_sensores as ps, eventos as ev
from .almacenamiento import guardar_influxdb as ei, guardar_log as rd


with open("config/config.json", encoding = "utf-8") as archivo:
    config = json.load(archivo)

segundos_entre_muestras = config["tiempo"]["espera_entre_muestras"]


def main(modo):

    valores_anteriores = {
        "temperatura": None,
        "humedad": None,
        "luz": None,
        "gas": None,
        "bateria": None,
        "corriente": None,
        "pitch": None,
        "roll": None,
        "distancia_frontal": None
    }

    modo_anterior = None

    variables = ["temperatura", "humedad", "luz", "gas", "bateria", "corriente", "pitch", "roll", "distancia_frontal"]


    while True:

        eventos = []


        # Obtener datos

        if modo == "simulado":

            datos = sd.generar_datos(config)
            eventos = ev.detectar_caida(datos, config, valores_anteriores["pitch"], valores_anteriores["roll"])

        else:

            datos_mqtt, conexion_ok = rm.recibir_mensaje()

            if datos_mqtt is not None:

                temperatura, humedad, luz, gas, pitch, roll, eventos_firmware = rm.preparar_datos(datos_mqtt)
                eventos = eventos_firmware

            else:

                temperatura = None
                humedad = None
                luz = None
                gas = None
                pitch = None
                roll = None

            datos = {
                "modo": "no_determinado",
                "conexion_ok": conexion_ok,
                "temperatura": temperatura,
                "humedad": humedad,
                "luz": luz,
                "gas": gas,
                "bateria": None,
                "corriente": None,
                "pitch": pitch,
                "roll": roll,
                "distancia_frontal": None
            }


        # Procesar datos

        estados = {}
        anomalias_simples = []

        for variable in variables:

            valor_anterior = valores_anteriores[variable]

            if modo == "fisico" and variable in ["bateria", "corriente", "distancia_frontal"]:
                estados[variable] = "NO_DISPONIBLE"
                continue

            if variable == "corriente" and modo_anterior is not None and datos["modo"] != modo_anterior:
                valor_anterior = None

            estado, anomalias = ps.procesar_variable(datos[variable], valor_anterior, config[variable], variable)

            estados[variable] = estado
            anomalias_simples += anomalias

        anomalias_complejas = ps.detectar_anomalias_complejas(estados["temperatura"], estados["gas"], estados["corriente"], estados["distancia_frontal"], datos["pitch"], valores_anteriores["pitch"], datos["roll"], valores_anteriores["roll"])

        hay_anomalia = bool(anomalias_simples or anomalias_complejas or eventos)


        # Guardar resultados

        registro = rd.registro(datos, modo, estados, anomalias_simples, anomalias_complejas, eventos, hay_anomalia)

        rd.guardar_log(registro, config)
        ei.enviar_registro_influx(registro, config)


        print("\nModo de datos:", modo)
        print("Modo de funcionamiento:", datos["modo"])
        print("Datos:", datos)
        print("Estados:", estados)
        print("Conexión:", datos["conexion_ok"])
        print("Hay anomalía:", hay_anomalia)
        print("Anomalías simples:", anomalias_simples)
        print("Anomalías complejas:", anomalias_complejas)
        print("Eventos:", eventos)
        print("----------------------------------------")


        for variable in valores_anteriores:

            if estados[variable] in ["SIN_DATOS", "INVALIDO", "FUERA_DE_RANGO", "NO_DISPONIBLE"]:
                valores_anteriores[variable] = None

            else:
                valores_anteriores[variable] = float(datos[variable])

        modo_anterior = datos["modo"]

        if modo == "simulado":
            time.sleep(segundos_entre_muestras)