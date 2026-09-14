import random


modo_actual = None
muestras_modo_restantes = 0
datos_anteriores = None


estado = {
    "temperatura": 32.0,
    "humedad": 50.0,
    "luz": 1400.0,
    "gas": 900.0,
    "bateria": 100.0,
    "corriente": 5.0,
    "pitch": 0.0,
    "roll": 0.0,
    "distancia_frontal": 300.0
}


def limitar(valor, minimo, maximo):

    if valor > maximo:
        return maximo

    elif valor < minimo:
        return minimo

    return valor


def elegir_modo():

    numero = random.randint(1, 100)

    if numero <= 35:
        modo = "reposo"

    elif numero <= 85:
        modo = "movimiento"

    else:
        modo = "esfuerzo"

    return modo


def generar_anomalia_simple(datos, config):

    variable = random.choice(["temperatura", "humedad", "luz", "gas", "corriente", "bateria", "pitch", "roll", "distancia_frontal"])


    if variable == "temperatura":

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["temperatura"] = config["temperatura"]["maximo"] + 20

        else:
            cambio = config["temperatura"]["umbral_cambio_brusco"] + 5

            if datos["temperatura"] + cambio <= config["temperatura"]["maximo"]:
                datos["temperatura"] = datos["temperatura"] + cambio

            else:
                datos["temperatura"] = datos["temperatura"] - cambio


    elif variable == "humedad":

        datos["humedad"] = config["humedad"]["maximo"] + 20


    elif variable == "luz":

        datos["luz"] = config["luz"]["maximo"] + 1000


    elif variable == "gas":

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["gas"] = config["gas"]["maximo"] + 500

        else:
            cambio = config["gas"]["umbral_cambio_brusco"] + 100
            datos["gas"] = datos["gas"] - cambio


    elif variable == "corriente":

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["corriente"] = config["corriente"]["maximo"] + 10

        else:
            datos["corriente"] = datos["corriente"] + config["corriente"]["umbral_cambio_brusco"] + 4


    elif variable == "bateria":

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["bateria"] = config["bateria"]["maximo"] + 10

        else:
            datos["bateria"] = datos["bateria"] - config["bateria"]["descarga_brusca"] - 5


    elif variable == "pitch":

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["pitch"] = config["pitch"]["maximo"] + 20

        else:
            datos["pitch"] = datos["pitch"] + config["pitch"]["umbral_cambio_brusco"] + 5


    elif variable == "roll":

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["roll"] = config["roll"]["maximo"] + 20

        else:
            datos["roll"] = datos["roll"] + config["roll"]["umbral_cambio_brusco"] + 5


    else:

        anomalia = random.randint(1, 2)

        if anomalia == 1:
            datos["distancia_frontal"] = config["distancia_frontal"]["maximo"] + 100

        else:
            cambio = config["distancia_frontal"]["umbral_cambio_brusco"] + 20

            if datos["distancia_frontal"] + cambio <= config["distancia_frontal"]["maximo"]:
                datos["distancia_frontal"] = datos["distancia_frontal"] + cambio

            else:
                datos["distancia_frontal"] = datos["distancia_frontal"] - cambio

    return datos


def generar_anomalia_compleja(datos, config, datos_anteriores):

    anomalia = random.randint(1, 2)


    # Incidente de gas

    if anomalia == 1:

        datos["temperatura"] = random.uniform(config["temperatura"]["umbral_alto"], config["temperatura"]["maximo"])
        datos["gas"] = random.uniform(config["gas"]["minimo"], config["gas"]["umbral_elevado"])


    # Atasco

    else:

        datos["corriente"] = random.uniform(config["corriente"]["umbral_critico"], 35)
        datos["distancia_frontal"] = random.uniform(config["distancia_frontal"]["minimo"], config["distancia_frontal"]["umbral_muy_cercano"] - 1)

        if datos_anteriores is not None:

            if datos_anteriores["pitch"] is not None:
                datos["pitch"] = datos_anteriores["pitch"]

            if datos_anteriores["roll"] is not None:
                datos["roll"] = datos_anteriores["roll"]

    return datos


def generar_caida(datos, config):

    eje = random.randint(1, 2)


    if eje == 1:

        if datos["pitch"] >= 0:
            datos["pitch"] = random.uniform(config["pitch"]["minimo"], -config["pitch"]["umbral_extremo"])

        else:
            datos["pitch"] = random.uniform(config["pitch"]["umbral_extremo"], config["pitch"]["maximo"])


    else:

        if datos["roll"] >= 0:
            datos["roll"] = random.uniform(config["roll"]["minimo"], -config["roll"]["umbral_extremo"])

        else:
            datos["roll"] = random.uniform(config["roll"]["umbral_extremo"], config["roll"]["maximo"])

    return datos


def generar_datos(config):

    global modo_actual, muestras_modo_restantes, datos_anteriores

    simulador = config["simulador"]


    # Modo de funcionamiento

    if modo_actual is None or muestras_modo_restantes == 0:
        modo_actual = elegir_modo()
        muestras_modo_restantes = random.randint(3, 6)

    modo = modo_actual
    muestras_modo_restantes = muestras_modo_restantes - 1


    if modo == "reposo":

        estado["corriente"] = random.uniform(1.0, 4.0)
        estado["bateria"] -= random.uniform(0.005, 0.02)

        estado["pitch"] += random.uniform(-0.3, 0.3)
        estado["roll"] += random.uniform(-0.3, 0.3)


    elif modo == "movimiento":

        estado["corriente"] = random.uniform(4.0, 10.0)
        estado["bateria"] -= random.uniform(0.05, 0.15)

        estado["pitch"] += random.uniform(-1.0, 1.0)
        estado["roll"] += random.uniform(-1.0, 1.0)


    else:

        estado["corriente"] = random.uniform(10.0, 20.0)
        estado["bateria"] -= random.uniform(0.15, 0.35)

        estado["pitch"] += random.uniform(-1.0, 1.0)
        estado["roll"] += random.uniform(-1.0, 1.0)


    # Variables del entorno

    estado["temperatura"] += random.uniform(-0.2, 0.2)
    estado["humedad"] += random.uniform(-0.5, 0.5)
    estado["luz"] += random.uniform(-100, 100)
    estado["gas"] += random.uniform(-20, 20)

    estado["distancia_frontal"] += random.uniform(-20, 20)


    # Limitar valores normales

    variables = ["temperatura", "humedad", "luz", "gas", "bateria", "corriente", "pitch", "roll", "distancia_frontal"]

    limites = [
        [simulador["temperatura_minima"], simulador["temperatura_maxima"]],
        [simulador["humedad_minima"], simulador["humedad_maxima"]],
        [simulador["luz_minima"], simulador["luz_maxima"]],
        [simulador["gas_minimo"], simulador["gas_maximo"]],
        [config["bateria"]["minimo"], config["bateria"]["maximo"]],
        [config["corriente"]["minimo"], 20],
        [simulador["pitch_minimo"], simulador["pitch_maximo"]],
        [simulador["roll_minimo"], simulador["roll_maximo"]],
        [simulador["distancia_frontal_minima"], simulador["distancia_frontal_maxima"]]
    ]

    for variable, limite in zip(variables, limites):
        estado[variable] = limitar(estado[variable], limite[0], limite[1])


    datos = estado.copy()


    # Conexión

    if random.randint(1, 100) <= simulador["probabilidad_desconexion"]:
        conexion_ok = False

    else:
        conexion_ok = True


    if conexion_ok == False:

        for variable in variables:
            datos[variable] = None


    else:

        numero = random.randint(1, 100)

        if numero <= simulador["probabilidad_anomalia_simple"]:
            datos = generar_anomalia_simple(datos, config)

        elif numero <= simulador["probabilidad_anomalia_simple"] + simulador["probabilidad_anomalia_compleja"]:
            datos = generar_anomalia_compleja(datos, config, datos_anteriores)

        elif numero <= simulador["probabilidad_anomalia_simple"] + simulador["probabilidad_anomalia_compleja"] + simulador["probabilidad_caida"]:
            datos = generar_caida(datos, config)


    # Redondear

    if conexion_ok:

        datos["temperatura"] = round(datos["temperatura"], 1)
        datos["humedad"] = round(datos["humedad"], 1)
        datos["luz"] = int(datos["luz"])
        datos["gas"] = int(datos["gas"])
        datos["bateria"] = int(datos["bateria"])
        datos["corriente"] = round(datos["corriente"], 2)
        datos["pitch"] = round(datos["pitch"], 2)
        datos["roll"] = round(datos["roll"], 2)
        datos["distancia_frontal"] = int(datos["distancia_frontal"])


    datos["conexion_ok"] = conexion_ok
    datos["modo"] = modo

    datos_anteriores = datos.copy()

    return datos

