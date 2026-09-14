from . import funciones_comunes as vs


def detectar_caida(datos, config, pitch_anterior, roll_anterior):

    eventos = []

    pitch_actual = datos.get("pitch")
    roll_actual = datos.get("roll")

    if pitch_actual is None or roll_actual is None:
        return eventos

    if pitch_anterior is None or roll_anterior is None:
        return eventos

    pitch_valido = not vs.detectar_fuera_de_rango(pitch_actual, config["pitch"]["minimo"], config["pitch"]["maximo"])
    roll_valido = not vs.detectar_fuera_de_rango(roll_actual, config["roll"]["minimo"], config["roll"]["maximo"])

    cambio_pitch = abs(pitch_actual - pitch_anterior)
    cambio_roll = abs(roll_actual - roll_anterior)

    caida_pitch = pitch_valido and abs(pitch_actual) >= config["pitch"]["umbral_extremo"] and cambio_pitch >= config["pitch"]["umbral_cambio_brusco"]
    caida_roll = roll_valido and abs(roll_actual) >= config["roll"]["umbral_extremo"] and cambio_roll >= config["roll"]["umbral_cambio_brusco"]

    if caida_pitch or caida_roll:
        eventos.append("posible_caida")

    return eventos