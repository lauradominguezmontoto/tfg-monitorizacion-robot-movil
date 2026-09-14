from . import funciones_comunes as vs


def procesar_variable(valor, valor_anterior, limites, tipo_variable):

    anomalias = []


    # Sin datos

    if vs.detectar_sin_datos(valor):
        return "SIN_DATOS", anomalias


    # Valor inválido

    if vs.detectar_valor_invalido(valor):
        anomalias.append(tipo_variable + "_invalido")
        return "INVALIDO", anomalias


    valor = float(valor)


    # Fuera de rango

    if vs.detectar_fuera_de_rango(valor, limites["minimo"], limites["maximo"]):
        anomalias.append(tipo_variable + "_fuera_de_rango")
        return "FUERA_DE_RANGO", anomalias


    # Batería

    if tipo_variable == "bateria":

        if valor <= limites["critica"]:
            estado = "BATERIA_MUY_BAJA"

        elif valor <= limites["baja"]:
            estado = "BATERIA_BAJA"

        else:
            estado = "NORMAL"


        if valor_anterior is not None:

            bajada = valor_anterior - valor

            if bajada >= limites["descarga_brusca"]:
                anomalias.append("descarga_brusca_bateria")

        return estado, anomalias


    # Pitch y roll

    if tipo_variable == "pitch" or tipo_variable == "roll":
        estado = vs.clasificar_sensor(valor, limites, "imu")


    # Resto de variables

    else:
        estado = vs.clasificar_sensor(valor, limites, tipo_variable)


    # Cambio brusco

    variables_cambio_brusco = ["temperatura", "gas", "corriente", "pitch", "roll", "distancia_frontal"]

    if tipo_variable in variables_cambio_brusco:

        cambio_brusco = vs.detectar_cambio_brusco(valor, valor_anterior, limites["umbral_cambio_brusco"])

        if cambio_brusco:

            if tipo_variable == "distancia_frontal":
                anomalias.append("cambio_brusco_distancia")

            else:
                anomalias.append("cambio_brusco_" + tipo_variable)


    return estado, anomalias


def detectar_anomalias_complejas(estado_temperatura, estado_gas, estado_corriente, estado_distancia_frontal, pitch, pitch_anterior, roll, roll_anterior):

    anomalias_complejas = []


    # Posible incidente de gas

    if estado_gas == "NIVEL_ELEVADO" and estado_temperatura == "AVISO_ALTO":
        anomalias_complejas.append("posible_incidente_gas")


    # Posible atasco

    pitch_estable = False
    roll_estable = False

    if pitch is not None and pitch_anterior is not None:
        pitch_estable = abs(pitch - pitch_anterior) <= 5

    if roll is not None and roll_anterior is not None:
        roll_estable = abs(roll - roll_anterior) <= 5


    if estado_corriente == "CORRIENTE_MUY_ALTA" and estado_distancia_frontal == "OBSTACULO_MUY_CERCANO" and pitch_estable and roll_estable:
        anomalias_complejas.append("posible_atasco")


    return anomalias_complejas