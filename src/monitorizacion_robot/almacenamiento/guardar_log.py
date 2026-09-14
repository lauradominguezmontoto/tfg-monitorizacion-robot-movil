import json
from datetime import datetime


def registro(datos, modo, estados, anomalias_simples, anomalias_complejas, eventos, hay_anomalia):

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    sensores = {
        "temperatura": datos["temperatura"],
        "humedad": datos["humedad"],
        "luz": datos["luz"],
        "gas": datos["gas"],
        "bateria": datos["bateria"],
        "corriente": datos["corriente"],
        "pitch": datos["pitch"],
        "roll": datos["roll"],
        "distancia_frontal": datos["distancia_frontal"]
    }

    registro_final = {
        "fecha_hora": fecha_hora,
        "id_dispositivo": "go2_logger_01",
        "modo_datos": modo,
        "modo_funcionamiento": datos["modo"],
        "conexion_ok": datos["conexion_ok"],
        "sensores": sensores,
        "estados": estados,
        "hay_anomalia": hay_anomalia,
        "anomalias_simples": anomalias_simples,
        "anomalias_complejas": anomalias_complejas,
        "eventos": eventos
    }

    return registro_final


def guardar_log(registro, config):

    ruta_log = config["archivos"]["log"]

    with open(ruta_log, "a", encoding = "utf-8") as archivo:
        json.dump(registro, archivo, ensure_ascii = False)
        archivo.write("\n")