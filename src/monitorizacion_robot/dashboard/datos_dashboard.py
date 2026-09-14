from src.monitorizacion_robot.almacenamiento.leer_influxdb import leer_influx


nombres_variables = {
    "temperatura": "Temperatura",
    "humedad": "Humedad",
    "luz": "Luz",
    "corriente": "Corriente",
    "gas": "Gas",
    "bateria": "Batería",
    "pitch": "Pitch",
    "roll": "Roll",
    "distancia_frontal": "Distancia frontal"
}

unidades = {
    "temperatura": "°C",
    "humedad": "%",
    "luz": "ADC",
    "corriente": "A",
    "gas": "ADC",
    "bateria": "%",
    "pitch": "°",
    "roll": "°",
    "distancia_frontal": "cm"
}


def valor_unidad(valor, variable):

    if valor is None:
        return "SIN DATOS"

    return str(valor) + " " + unidades[variable]


def datos_anomalia(anomalia):

    if anomalia == "posible_incidente_gas":
        valores = "Temperatura, Gas"
        descripcion = "Gas elevado + calor"

    elif anomalia == "posible_atasco":
        valores = "Corriente, Distancia frontal, Pitch, Roll"
        descripcion = "Esfuerzo sin avance"

    elif anomalia == "posible_caida":
        valores = "Pitch, Roll"
        descripcion = "Inclinación + cambio brusco"

    else:
        valores = "-"
        descripcion = "-"

    return valores, descripcion


def datos_inicio(config):

    datos_influx = leer_influx(config, "telemetria")

    if len(datos_influx) == 0:
        return {}, {}, {}

    valores = {}
    estados = {}

    # Último valor de cada variable

    for dato in datos_influx:

        variable = dato.get("variable")

        if variable in nombres_variables and variable not in valores:
            valores[variable] = dato.get("valor")
            estados[variable] = dato.get("estado")

    ultimo_dato = datos_influx[0]

    informacion = {
        "fecha_hora": ultimo_dato.get("fecha_hora"),
        "id_dispositivo": ultimo_dato.get("id_dispositivo"),
        "modo_datos": ultimo_dato.get("modo_datos"),
        "modo_funcionamiento": ultimo_dato.get("modo_funcionamiento"),
        "conexion_ok": ultimo_dato.get("conexion_ok"),
        "hay_anomalia": ultimo_dato.get("hay_anomalia")
    }

    return valores, estados, informacion


def datos_dashboard(config, tipo, variable = None):

    if tipo == "anomalias_complejas":
        datos_influx = leer_influx(config, "eventos")

    else:
        datos_influx = leer_influx(config, "telemetria")

    datos_preparados = []

    # Historial

    if tipo == "historial":

        for dato_influx in datos_influx:

            if dato_influx.get("variable") == variable:

                hora = dato_influx["fecha_hora"].astimezone().strftime("%H:%M:%S")
                valor = dato_influx.get("valor")

                datos_preparados.append((hora, valor))

                if len(datos_preparados) == config["dashboard"]["max_historial"]:
                    break

        datos_preparados.reverse()

        return datos_preparados

    for dato_influx in datos_influx:

        if tipo == "anomalias_complejas":

            anomalia = dato_influx.get("anomalia_compleja")

            if anomalia is None:
                anomalia = dato_influx.get("evento")

            if anomalia is None:
                continue

            fecha_hora = dato_influx["fecha_hora"].astimezone().strftime("%d/%m %H:%M:%S")
            valores, descripcion = datos_anomalia(anomalia)

            dato_preparado = (fecha_hora, anomalia, valores, descripcion)

        elif tipo == "lecturas":

            variable_dato = dato_influx.get("variable")

            if variable_dato not in nombres_variables:
                continue

            fecha_hora = dato_influx["fecha_hora"].astimezone().strftime("%d/%m %H:%M:%S")
            nombre_variable = nombres_variables[variable_dato]
            valor = valor_unidad(dato_influx.get("valor"), variable_dato)
            estado = dato_influx.get("estado")

            dato_preparado = (fecha_hora, nombre_variable, valor, estado)

        else:

            anomalia = dato_influx.get("anomalia_simple")

            if anomalia is None or anomalia == "NINGUNA":
                continue

            variable_dato = dato_influx.get("variable")

            if variable_dato not in nombres_variables:
                continue

            fecha_hora = dato_influx["fecha_hora"].astimezone().strftime("%d/%m %H:%M:%S")
            nombre_variable = nombres_variables[variable_dato]
            valor = valor_unidad(dato_influx.get("valor"), variable_dato)

            dato_preparado = (fecha_hora, nombre_variable, valor, anomalia)

        datos_preparados.append(dato_preparado)

        if len(datos_preparados) == config["dashboard"]["max_filas"]:
            break

    return datos_preparados