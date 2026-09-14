"""
Recepción de datos mediante MQTT.
"""

import json
import queue

from paho.mqtt import client as mqtt


with open("config/config.json", encoding = "utf-8") as archivo:
    config = json.load(archivo)

broker = config["mqtt"]["broker"]
puerto = config["mqtt"]["puerto"]
tema = config["mqtt"]["tema_sensores"]

tiempo_espera = 15

cola_mensajes = queue.Queue()

cliente = None
mqtt_iniciado = False


def al_conectar(cliente, userdata, flags, reason_code, properties):

    if reason_code == 0:
        cliente.subscribe(tema)
        print("MQTT conectado")

    else:
        print("No se pudo conectar con MQTT")


def al_recibir(cliente, userdata, mensaje):

    texto = str(mensaje.payload, "utf-8")
    cola_mensajes.put(texto)


def iniciar_mqtt():

    global cliente
    global mqtt_iniciado

    if mqtt_iniciado:
        return True

    try:
        cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        cliente.on_connect = al_conectar
        cliente.on_message = al_recibir

        cliente.connect(broker, puerto, 60)
        cliente.loop_start()

        mqtt_iniciado = True

        return True

    except Exception as error:
        print("No se pudo conectar con MQTT")
        print(error)

        return False


def recibir_mensaje():

    conexion_mqtt = iniciar_mqtt()

    if not conexion_mqtt:
        return None, False

    try:
        texto = cola_mensajes.get(timeout = tiempo_espera)

    except queue.Empty:
        return None, False

    try:
        datos = json.loads(texto)

        return datos, True

    except json.JSONDecodeError:
        print("No se pudo leer el mensaje")

        return None, False


def preparar_datos(datos):

    temperatura = datos.get("temperatura")
    humedad = datos.get("humedad")
    luz = datos.get("luz")
    gas = datos.get("gas")
    pitch = datos.get("pitch")
    roll = datos.get("roll")

    eventos_firmware = []

    if datos.get("posible_caida") == True:
        eventos_firmware.append("posible_caida")

    return temperatura, humedad, luz, gas, pitch, roll, eventos_firmware