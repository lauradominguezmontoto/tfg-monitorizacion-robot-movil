def detectar_cambio_brusco(valor_actual, valor_anterior, umbral):

    if valor_anterior is None:
        hay_cambio_brusco = False

    else:
        diferencia = abs(valor_actual - valor_anterior)

        if diferencia >= umbral:
            hay_cambio_brusco = True

        else:
            hay_cambio_brusco = False

    return hay_cambio_brusco


def detectar_fuera_de_rango(valor, minimo, maximo):

    if valor < minimo or valor > maximo:
        esta_fuera_de_rango = True

    else:
        esta_fuera_de_rango = False

    return esta_fuera_de_rango


def detectar_sin_datos(valor):

    if valor is None or valor == "":
        return True

    return False


def detectar_valor_invalido(valor):

    try:
        float(valor)
        return False

    except (ValueError, TypeError):
        return True


def clasificar_sensor(valor, limites, tipo_sensor):

    if tipo_sensor == "temperatura" or tipo_sensor == "humedad":

        if valor <= limites["umbral_bajo"]:
            estado = "AVISO_BAJO"

        elif valor >= limites["umbral_alto"]:
            estado = "AVISO_ALTO"

        else:
            estado = "NORMAL"


    elif tipo_sensor == "luz":

        if valor <= limites["umbral_bajo"]:
            estado = "ILUMINACION_BAJA"

        elif valor >= limites["umbral_alto"]:
            estado = "ILUMINACION_ALTA"

        else:
            estado = "NORMAL"


    elif tipo_sensor == "corriente":

        if valor >= limites["umbral_critico"]:
            estado = "CORRIENTE_MUY_ALTA"

        elif valor >= limites["umbral_alto"]:
            estado = "CORRIENTE_ALTA"

        else:
            estado = "NORMAL"


    elif tipo_sensor == "imu":

        valor_abs = abs(valor)

        if valor_abs < limites["umbral_aviso"]:
            estado = "NORMAL"

        elif valor_abs < limites["umbral_critico"]:
            estado = "INCLINACION_ELEVADA"

        elif valor_abs < limites["umbral_extremo"]:
            estado = "INCLINACION_MUY_ELEVADA"

        else:
            estado = "INCLINACION_EXTREMA"


    elif tipo_sensor == "gas":

        if valor <= limites["umbral_elevado"]:
            estado = "NIVEL_ELEVADO"

        elif valor <= limites["umbral_detectado"]:
            estado = "PRESENCIA_DETECTADA"

        else:
            estado = "NORMAL"


    elif tipo_sensor == "distancia_frontal":

        if valor < limites["umbral_muy_cercano"]:
            estado = "OBSTACULO_MUY_CERCANO"

        elif valor < limites["umbral_cercano"]:
            estado = "OBSTACULO_CERCANO"

        else:
            estado = "NORMAL"


    else:
        estado = "ERROR"

    return estado