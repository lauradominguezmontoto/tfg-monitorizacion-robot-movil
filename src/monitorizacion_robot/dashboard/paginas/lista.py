from py_simple_ttk.widgets.WidgetsCore import create_round_rectangle

from src.monitorizacion_robot.dashboard.aspecto_dashboard import color_tarjetas, color_azul_claro, color_azul_oscuro, color_texto, color_estado_normal, color_estado_aviso, color_estado_critico, fuente_grande, fuente_mediana, fuente_pequena
from src.monitorizacion_robot.dashboard import idiomas_dashboard as idiomas


radio_fondo = 26
radio_cabecera_tabla = 14

x_fecha = 315
x_columna_2 = 500
x_columna_3 = 730
x_columna_4 = 1000


def obtener_color_estado(estado):

    if estado == "NORMAL":
        return color_estado_normal

    elif estado in ["AVISO", "AVISO_BAJO", "AVISO_ALTO", "ILUMINACION_BAJA", "ILUMINACION_ALTA", "CORRIENTE_ALTA", "BATERIA_BAJA", "INCLINACION_ELEVADA", "PRESENCIA_DETECTADA", "OBSTACULO_CERCANO"]:
        return color_estado_aviso

    elif estado in ["CORRIENTE_MUY_ALTA", "BATERIA_MUY_BAJA", "INCLINACION_MUY_ELEVADA", "INCLINACION_EXTREMA", "NIVEL_ELEVADO", "OBSTACULO_MUY_CERCANO", "INVALIDO", "FUERA_DE_RANGO"]:
        return color_estado_critico

    return color_texto


def textos_lista(tipo):

    if tipo == "lecturas":

        titulo = "Lecturas"
        subtitulo = "Últimas lecturas recibidas"

        columna_2 = "Variable"
        columna_3 = "Valor"
        columna_4 = "Estado"

    elif tipo == "anomalias_simples":

        titulo = "Anomalías simples"
        subtitulo = "Últimas anomalías detectadas"

        columna_2 = "Variable"
        columna_3 = "Valor"
        columna_4 = "Anomalía"

    else:

        titulo = "Anomalías complejas"
        subtitulo = "Últimas anomalías complejas y eventos detectados"

        columna_2 = "Anomalía"
        columna_3 = "Valores implicados"
        columna_4 = "Descripción"

    titulos = [
        (idiomas.traducir("Fecha y hora"), x_fecha),
        (idiomas.traducir(columna_2), x_columna_2),
        (idiomas.traducir(columna_3), x_columna_3),
        (idiomas.traducir(columna_4), x_columna_4)
    ]

    titulo = idiomas.traducir(titulo)
    subtitulo = idiomas.traducir(subtitulo)

    return titulo, subtitulo, titulos


def lista(dashboard, tipo, datos):

    titulo, subtitulo, titulos = textos_lista(tipo)

    create_round_rectangle(dashboard, 220, 110, 1160, 640, r = radio_fondo, fill = color_tarjetas, outline = "")

    dashboard.create_text(250, 140, text = titulo, font = fuente_grande, fill = color_texto, anchor = "w")
    dashboard.create_text(250, 170, text = subtitulo, font = fuente_pequena, fill = color_texto, anchor = "w")

    create_round_rectangle(dashboard, 240, 190, 1140, 230, r = radio_cabecera_tabla, fill = color_azul_claro, outline = "")

    for texto, x in titulos:
        dashboard.create_text(x, 210, text = texto, font = fuente_mediana, fill = color_texto)

    y = 255

    for fila in datos:

        color_2 = color_texto
        color_4 = color_texto

        if tipo == "lecturas":

            fecha_hora, variable, valor, estado = fila

            columna_2 = idiomas.traducir(variable)
            columna_3 = valor
            columna_4 = idiomas.traducir(estado)

            color_4 = obtener_color_estado(estado)

        elif tipo == "anomalias_simples":

            fecha_hora, variable, valor, anomalia = fila

            columna_2 = idiomas.traducir(variable)
            columna_3 = valor
            columna_4 = idiomas.traducir(anomalia)

            color_4 = color_estado_critico

        else:

            fecha_hora, anomalia, valores, descripcion = fila

            columna_2 = idiomas.traducir(anomalia)
            columna_3 = idiomas.traducir(valores)
            columna_4 = idiomas.traducir(descripcion)

            color_2 = color_estado_critico

        dashboard.create_text(x_fecha, y, text = fecha_hora, font = fuente_pequena, fill = color_texto)
        dashboard.create_text(x_columna_2, y, text = columna_2, font = fuente_pequena, fill = color_2)
        dashboard.create_text(x_columna_3, y, text = columna_3, font = fuente_pequena, fill = color_texto)
        dashboard.create_text(x_columna_4, y, text = columna_4, font = fuente_pequena, fill = color_4)

        dashboard.create_line(250, y + 18, 1130, y + 18, fill = color_azul_oscuro)

        y = y + 43