import json
import time
import tkinter as tk

from py_simple_ttk.widgets.WidgetsCore import create_round_rectangle

from src.monitorizacion_robot.dashboard.aspecto_dashboard import *
from src.monitorizacion_robot.dashboard.datos_dashboard import datos_inicio, datos_dashboard
from src.monitorizacion_robot.dashboard.paginas.inicio import inicio
from src.monitorizacion_robot.dashboard.paginas.variables import variables
from src.monitorizacion_robot.dashboard.paginas.lista import lista
from src.monitorizacion_robot.dashboard import idiomas_dashboard as idiomas


with open("config/config.json", encoding = "utf-8") as archivo:
    config = json.load(archivo)


# Datos del dashboard

valores = {
    "temperatura": None,
    "humedad": None,
    "luz": None,
    "corriente": None,
    "gas": None,
    "bateria": None,
    "pitch": None,
    "roll": None,
    "distancia_frontal": None
}

estados = {
    "temperatura": "SIN_DATOS",
    "humedad": "SIN_DATOS",
    "luz": "SIN_DATOS",
    "corriente": "SIN_DATOS",
    "gas": "SIN_DATOS",
    "bateria": "SIN_DATOS",
    "pitch": "SIN_DATOS",
    "roll": "SIN_DATOS",
    "distancia_frontal": "SIN_DATOS"
}

variables_monitorizadas = list(valores.keys())

lecturas = []
anomalias_simples = []
anomalias_complejas = []
informacion = {}

variable_seleccionada = "temperatura"
historial_variable = []

pagina = "inicio"


# Ventana

ventana = tk.Tk()

ventana.title(idiomas.traducir("Dashboard de monitorización"))
ventana.geometry(str(ancho_dashboard) + "x" + str(alto_dashboard))
ventana.resizable(False, False)

dashboard = tk.Canvas(ventana, width = ancho_dashboard, height = alto_dashboard, bg = color_dashboard)
dashboard.pack()


# Cabecera

def cabecera():

    radio_cabecera = 26

    create_round_rectangle(dashboard, 18, 10, ancho_dashboard - 18, alto_cabecera - 10, r = radio_cabecera, fill = color_azul_claro, outline = "")

    hora = time.strftime("%H:%M:%S")
    fecha = time.strftime("%d/%m/%Y")

    dashboard.create_text(40, alto_cabecera / 2, text = idiomas.traducir("Dashboard de monitorización del robot"), font = fuente_grande, fill = color_texto_claro, anchor = "w")
    dashboard.create_text(ancho_dashboard - 40, 30, text = hora, font = fuente_mediana, fill = color_texto_claro, anchor = "e")
    dashboard.create_text(ancho_dashboard - 40, 52, text = fecha, font = fuente_pequena, fill = color_texto_claro, anchor = "e")


def ir_a_pagina(nueva_pagina):

    global pagina

    pagina = nueva_pagina
    dibujar()


def cambiar_idioma_dashboard(nuevo_idioma):

    idiomas.cambiar_idioma(nuevo_idioma)
    ventana.title(idiomas.traducir("Dashboard de monitorización"))
    dibujar()


# Menú

def menu():

    radio_menu = 26

    ancho_boton = 150
    alto_boton = 34
    x_boton = 34

    fuente_boton_menu = ("Segoe UI", 9)

    ancho_boton_idioma = 40
    alto_boton_idioma = 30

    x_es = 34
    x_en = 89
    x_gl = 144

    y_idioma = alto_dashboard - 65

    create_round_rectangle(dashboard, 18, alto_cabecera, ancho_menu, alto_dashboard - 18, r = radio_menu, fill = color_azul_oscuro, outline = "")

    y_inicio = 115
    y_variables = 190
    y_lecturas = 265
    y_anomalias_simples = 340
    y_anomalias_complejas = 415

    def ir_inicio():
        ir_a_pagina("inicio")

    def ir_variables():
        ir_a_pagina("variables")

    def ir_lecturas():
        ir_a_pagina("lecturas")

    def ir_anomalias_simples():
        ir_a_pagina("anomalias_simples")

    def ir_anomalias_complejas():
        ir_a_pagina("anomalias_complejas")

    boton_inicio = tk.Button(dashboard, text = idiomas.traducir("INICIO"), command = ir_inicio, bg = color_boton_seleccionado if pagina == "inicio" else color_botones, fg = color_texto, font = fuente_boton_menu, relief = "flat", borderwidth = 0)
    boton_inicio.place(x = x_boton, y = y_inicio, width = ancho_boton, height = alto_boton)

    boton_variables = tk.Button(dashboard, text = idiomas.traducir("VARIABLES"), command = ir_variables, bg = color_boton_seleccionado if pagina == "variables" else color_botones, fg = color_texto, font = fuente_boton_menu, relief = "flat", borderwidth = 0)
    boton_variables.place(x = x_boton, y = y_variables, width = ancho_boton, height = alto_boton)

    boton_lecturas = tk.Button(dashboard, text = idiomas.traducir("LECTURAS"), command = ir_lecturas, bg = color_boton_seleccionado if pagina == "lecturas" else color_botones, fg = color_texto, font = fuente_boton_menu, relief = "flat", borderwidth = 0)
    boton_lecturas.place(x = x_boton, y = y_lecturas, width = ancho_boton, height = alto_boton)

    boton_anomalias_simples = tk.Button(dashboard, text = idiomas.traducir("ANOMALÍAS SIMPLES"), command = ir_anomalias_simples, bg = color_boton_seleccionado if pagina == "anomalias_simples" else color_botones, fg = color_texto, font = fuente_boton_menu, relief = "flat", borderwidth = 0)
    boton_anomalias_simples.place(x = x_boton, y = y_anomalias_simples, width = ancho_boton, height = alto_boton)

    boton_anomalias_complejas = tk.Button(dashboard, text = idiomas.traducir("ANOMALÍAS COMPLEJAS"), command = ir_anomalias_complejas, bg = color_boton_seleccionado if pagina == "anomalias_complejas" else color_botones, fg = color_texto, font = fuente_boton_menu, relief = "flat", borderwidth = 0)
    boton_anomalias_complejas.place(x = x_boton, y = y_anomalias_complejas, width = ancho_boton, height = alto_boton)

    def poner_espanol():
        cambiar_idioma_dashboard("ES")

    def poner_ingles():
        cambiar_idioma_dashboard("EN")

    def poner_gallego():
        cambiar_idioma_dashboard("GL")

    color_es = color_botones
    color_en = color_botones
    color_gl = color_botones

    if idiomas.obtener_idioma() == "ES":
        color_es = color_azul_claro

    elif idiomas.obtener_idioma() == "EN":
        color_en = color_azul_claro

    elif idiomas.obtener_idioma() == "GL":
        color_gl = color_azul_claro

    botones_idioma = [
        ("ES", poner_espanol, color_es, x_es),
        ("EN", poner_ingles, color_en, x_en),
        ("GL", poner_gallego, color_gl, x_gl)
    ]

    for texto, funcion, color, x in botones_idioma:

        boton = tk.Button(dashboard, text = texto, command = funcion, bg = color, fg = color_texto, font = fuente_boton_menu, relief = "flat", borderwidth = 0)
        boton.place(x = x, y = y_idioma, width = ancho_boton_idioma, height = alto_boton_idioma)


def ir_a_variable(nueva_variable):

    global variable_seleccionada, historial_variable

    variable_seleccionada = nueva_variable
    historial_variable = []

    dibujar()


# Dibujar dashboard

def dibujar():

    for elemento in dashboard.winfo_children():
        elemento.destroy()

    dashboard.delete("all")

    cabecera()
    menu()

    if pagina == "inicio":
        inicio(dashboard, valores, estados, informacion)

    elif pagina == "variables":
        variables(dashboard, ir_a_variable, variable_seleccionada, historial_variable, config)

    elif pagina == "lecturas":
        lista(dashboard, "lecturas", lecturas)

    elif pagina == "anomalias_simples":
        lista(dashboard, "anomalias_simples", anomalias_simples)

    elif pagina == "anomalias_complejas":
        lista(dashboard, "anomalias_complejas", anomalias_complejas)


# Actualizar datos

def actualizar():

    global valores, estados, lecturas, anomalias_simples, anomalias_complejas, informacion, historial_variable

    redibujar = False

    if pagina == "inicio":

        nuevos_valores, nuevos_estados, nueva_informacion = datos_inicio(config)
        modo = nueva_informacion.get("modo_datos")

        for variable in variables_monitorizadas:

            if variable not in nuevos_valores:
                nuevos_valores[variable] = None

            if variable not in nuevos_estados:

                if modo == "fisico" and variable in ["corriente", "bateria", "distancia_frontal"]:
                    nuevos_estados[variable] = "NO_DISPONIBLE"

                else:
                    nuevos_estados[variable] = "SIN_DATOS"

        valores = nuevos_valores
        estados = nuevos_estados
        informacion = nueva_informacion

        redibujar = True

    elif pagina == "variables":

        nuevo_historial = datos_dashboard(config, "historial", variable_seleccionada)

        if nuevo_historial != historial_variable:
            historial_variable = nuevo_historial
            redibujar = True

    elif pagina == "lecturas":

        nuevas_lecturas = datos_dashboard(config, "lecturas")

        if nuevas_lecturas != lecturas:
            lecturas = nuevas_lecturas
            redibujar = True

    elif pagina == "anomalias_simples":

        nuevas_anomalias_simples = datos_dashboard(config, "anomalias_simples")

        if nuevas_anomalias_simples != anomalias_simples:
            anomalias_simples = nuevas_anomalias_simples
            redibujar = True

    elif pagina == "anomalias_complejas":

        nuevas_anomalias_complejas = datos_dashboard(config, "anomalias_complejas")

        if nuevas_anomalias_complejas != anomalias_complejas:
            anomalias_complejas = nuevas_anomalias_complejas
            redibujar = True

    if redibujar:
        dibujar()

    ventana.after(config["dashboard"]["actualizacion_ms"], actualizar)


dibujar()
actualizar()

ventana.mainloop()