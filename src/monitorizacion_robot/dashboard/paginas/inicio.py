from py_simple_ttk.widgets.WidgetsCore import create_round_rectangle

from src.monitorizacion_robot.dashboard.aspecto_dashboard import ancho_menu, alto_cabecera, ancho_dashboard, alto_dashboard, color_tarjetas, color_botones, color_azul_oscuro, color_texto, color_estado_normal, color_estado_aviso, color_estado_critico, fuente_mediana, fuente_mediana_negrita, fuente_tarjeta, fuente_valor, fuente_estado
from src.monitorizacion_robot.dashboard import idiomas_dashboard as idiomas


ancho_zona = 210
ancho_imu = ancho_zona * 2 + 30

alto_zona = 200
separacion = 30

radio_tarjetas = 26
radio_titulos = 12


def obtener_color_estado(estado):

    if estado == "NORMAL":
        return color_estado_normal

    elif estado in ["AVISO", "AVISO_BAJO", "AVISO_ALTO", "ILUMINACION_BAJA", "ILUMINACION_ALTA", "CORRIENTE_ALTA", "BATERIA_BAJA", "INCLINACION_ELEVADA", "PRESENCIA_DETECTADA", "OBSTACULO_CERCANO"]:
        return color_estado_aviso

    elif estado in ["CORRIENTE_MUY_ALTA", "BATERIA_MUY_BAJA", "INCLINACION_MUY_ELEVADA", "INCLINACION_EXTREMA", "NIVEL_ELEVADO", "OBSTACULO_MUY_CERCANO", "INVALIDO", "FUERA_DE_RANGO"]:
        return color_estado_critico

    return color_texto


def mostrar_variable(dashboard, x, y, nombre_variable, valor, unidad, estado):

    create_round_rectangle(dashboard, x, y, x + ancho_zona, y + alto_zona, r = radio_tarjetas, fill = color_tarjetas, outline = "")

    create_round_rectangle(dashboard, x + 25, y + 20, x + ancho_zona - 25, y + 52, r = radio_titulos, fill = color_botones, outline = "")

    dashboard.create_text(x + ancho_zona / 2, y + 36, text = idiomas.traducir(nombre_variable), font = fuente_tarjeta, fill = color_texto)

    if estado == "NO_DISPONIBLE":

        dashboard.create_text(x + ancho_zona / 2, y + 102, text = idiomas.traducir("NO DISPONIBLE"), font = fuente_valor, fill = color_texto)

    elif valor is None:

        dashboard.create_text(x + ancho_zona / 2, y + 102, text = idiomas.traducir("SIN DATOS"), font = fuente_valor, fill = color_texto)

    elif unidad == "ADC":

        dashboard.create_text(x + ancho_zona / 2, y + 92, text = str(valor), font = fuente_valor, fill = color_texto)
        dashboard.create_text(x + ancho_zona / 2, y + 120, text = "ADC", font = fuente_tarjeta, fill = color_texto)

    else:

        valor_texto = str(valor) + " " + unidad

        dashboard.create_text(x + ancho_zona / 2, y + 102, text = valor_texto, font = fuente_valor, fill = color_texto)

    dashboard.create_line(x + 25, y + 137, x + ancho_zona - 25, y + 137, fill = color_azul_oscuro)

    color_estado = obtener_color_estado(estado)

    dashboard.create_text(x + ancho_zona / 2, y + 164, text = idiomas.traducir(estado), font = fuente_estado, fill = color_estado)


def mostrar_imu(dashboard, x, y, valores, estados):

    create_round_rectangle(dashboard, x, y, x + ancho_imu, y + alto_zona, r = radio_tarjetas, fill = color_tarjetas, outline = "")

    create_round_rectangle(dashboard, x + 140, y + 20, x + ancho_imu - 140, y + 52, r = radio_titulos, fill = color_botones, outline = "")

    dashboard.create_text(x + ancho_imu / 2, y + 36, text = "IMU", font = fuente_tarjeta, fill = color_texto)

    dashboard.create_line(x + ancho_imu / 2, y + 60, x + ancho_imu / 2, y + 182, fill = color_azul_oscuro)

    x_pitch = x + ancho_imu / 4
    color_pitch = obtener_color_estado(estados["pitch"])

    if valores["pitch"] is None:
        valor_pitch = idiomas.traducir("SIN DATOS")

    else:
        valor_pitch = str(valores["pitch"]) + " °"

    dashboard.create_text(x_pitch, y + 70, text = "PITCH", font = fuente_tarjeta, fill = color_texto)
    dashboard.create_text(x_pitch, y + 102, text = valor_pitch, font = fuente_valor, fill = color_texto)

    dashboard.create_line(x_pitch - 75, y + 137, x_pitch + 75, y + 137, fill = color_azul_oscuro)

    dashboard.create_text(x_pitch, y + 164, text = idiomas.traducir(estados["pitch"]), font = fuente_estado, fill = color_pitch)

    x_roll = x + ancho_imu * 3 / 4
    color_roll = obtener_color_estado(estados["roll"])

    if valores["roll"] is None:
        valor_roll = idiomas.traducir("SIN DATOS")

    else:
        valor_roll = str(valores["roll"]) + " °"

    dashboard.create_text(x_roll, y + 70, text = "ROLL", font = fuente_tarjeta, fill = color_texto)
    dashboard.create_text(x_roll, y + 102, text = valor_roll, font = fuente_valor, fill = color_texto)

    dashboard.create_line(x_roll - 75, y + 137, x_roll + 75, y + 137, fill = color_azul_oscuro)

    dashboard.create_text(x_roll, y + 164, text = idiomas.traducir(estados["roll"]), font = fuente_estado, fill = color_roll)


def inicio(dashboard, valores, estados, informacion):

    alto_info = 60

    ancho_total = ancho_zona * 4 + separacion * 3
    alto_total = alto_info + separacion + alto_zona + separacion + alto_zona

    x_primera = ancho_menu + (ancho_dashboard - ancho_menu - ancho_total) / 2
    y_info = alto_cabecera + (alto_dashboard - alto_cabecera - alto_total) / 2

    x_segunda = x_primera + ancho_zona + separacion
    x_tercera = x_segunda + ancho_zona + separacion
    x_cuarta = x_tercera + ancho_zona + separacion

    y_primera = y_info + alto_info + separacion
    y_segunda = y_primera + alto_zona + separacion


    # Información general

    create_round_rectangle(dashboard, x_primera, y_info, x_primera + ancho_total, y_info + alto_info, r = radio_tarjetas, fill = color_tarjetas, outline = "")

    ancho_info = ancho_total / 3

    x_linea_1 = x_primera + ancho_info
    x_linea_2 = x_primera + ancho_info * 2

    dashboard.create_line(x_linea_1, y_info + 13, x_linea_1, y_info + alto_info - 13, fill = color_azul_oscuro)
    dashboard.create_line(x_linea_2, y_info + 13, x_linea_2, y_info + alto_info - 13, fill = color_azul_oscuro)

    y_texto = y_info + alto_info / 2

    modo_datos = informacion.get("modo_datos")

    if modo_datos == "simulado":
        modo = idiomas.traducir("Simulación")

    elif modo_datos == "fisico":
        modo = idiomas.traducir("Físico")

    else:
        modo = idiomas.traducir("SIN DATOS")

    x_modo = x_primera + ancho_info / 2

    dashboard.create_text(x_modo - 5, y_texto, text = idiomas.traducir("Modo") + ":", font = fuente_mediana_negrita, fill = color_texto, anchor = "e")
    dashboard.create_text(x_modo + 5, y_texto, text = modo, font = fuente_mediana, fill = color_texto, anchor = "w")

    conexion_ok = informacion.get("conexion_ok")

    if conexion_ok == True or conexion_ok == "True":
        conexion = "OK"
        color_conexion = color_estado_normal

    elif conexion_ok == False or conexion_ok == "False":
        conexion = idiomas.traducir("PERDIDA")
        color_conexion = color_estado_critico

    else:
        conexion = idiomas.traducir("SIN DATOS")
        color_conexion = color_texto

    x_conexion = x_primera + ancho_info + ancho_info / 2

    dashboard.create_text(x_conexion - 5, y_texto, text = idiomas.traducir("Conexión") + ":", font = fuente_mediana_negrita, fill = color_texto, anchor = "e")
    dashboard.create_text(x_conexion + 5, y_texto, text = conexion, font = fuente_mediana, fill = color_conexion, anchor = "w")

    color_bateria = obtener_color_estado(estados["bateria"])

    if estados["bateria"] == "NO_DISPONIBLE":
        bateria = idiomas.traducir("NO DISPONIBLE")

    elif valores["bateria"] is None:
        bateria = idiomas.traducir("SIN DATOS")

    else:
        bateria = str(valores["bateria"]) + " %"

    x_bateria = x_primera + ancho_info * 2 + ancho_info / 2

    dashboard.create_text(x_bateria - 5, y_texto, text = idiomas.traducir("Batería") + ":", font = fuente_mediana_negrita, fill = color_texto, anchor = "e")
    dashboard.create_text(x_bateria + 5, y_texto, text = bateria, font = fuente_mediana, fill = color_bateria, anchor = "w")


    # Variables

    mostrar_variable(dashboard, x_primera, y_primera, "GAS", valores["gas"], "ADC", estados["gas"])
    mostrar_variable(dashboard, x_segunda, y_primera, "HUMEDAD", valores["humedad"], "%", estados["humedad"])
    mostrar_variable(dashboard, x_tercera, y_primera, "LUZ", valores["luz"], "ADC", estados["luz"])
    mostrar_variable(dashboard, x_cuarta, y_primera, "TEMPERATURA", valores["temperatura"], "°C", estados["temperatura"])

    mostrar_variable(dashboard, x_primera, y_segunda, "CORRIENTE", valores["corriente"], "A", estados["corriente"])
    mostrar_variable(dashboard, x_segunda, y_segunda, "DISTANCIA FRONTAL", valores["distancia_frontal"], "cm", estados["distancia_frontal"])

    mostrar_imu(dashboard, x_tercera, y_segunda, valores, estados)