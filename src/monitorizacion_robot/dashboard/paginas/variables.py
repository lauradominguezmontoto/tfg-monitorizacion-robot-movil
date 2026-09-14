import tkinter as tk
from py_simple_ttk.widgets.WidgetsCore import create_round_rectangle

from src.monitorizacion_robot.dashboard.aspecto_dashboard import ancho_menu, alto_cabecera, ancho_dashboard, color_tarjetas, color_azul_claro, color_azul_oscuro, color_botones, color_texto, fuente_grande, fuente_mediana, fuente_pequena
from src.monitorizacion_robot.dashboard.datos_dashboard import nombres_variables, unidades
from src.monitorizacion_robot.dashboard import idiomas_dashboard as idiomas


ancho_boton = 160
alto_boton = 40
separacion_botones = 22

radio_grafica = 26

variables_monitorizadas = ["temperatura", "humedad", "corriente", "luz", "gas", "bateria", "pitch", "roll", "distancia_frontal"]


def grafica(dashboard, variable_seleccionada, historial_variable, config):

    create_round_rectangle(dashboard, 240, 235, 1140, 640, r = radio_grafica, fill = color_tarjetas, outline = "")

    nombre = nombres_variables[variable_seleccionada]

    dashboard.create_text(275, 270, text = idiomas.traducir(nombre), font = fuente_grande, fill = color_texto, anchor = "w")


    # Datos válidos

    datos_validos = []

    for hora, valor in historial_variable:

        if valor is not None:
            datos_validos.append((hora, float(valor)))

    if len(datos_validos) == 0:

        dashboard.create_text(690, 440, text = idiomas.traducir("SIN DATOS"), font = fuente_mediana, fill = color_texto)

        return


    ultimo_valor = datos_validos[-1][1]

    dashboard.create_text(1090, 260, text = idiomas.traducir("Último valor"), font = fuente_pequena, fill = color_texto, anchor = "e")
    dashboard.create_text(1090, 290, text = str(ultimo_valor) + " " + unidades[variable_seleccionada], font = fuente_mediana, fill = color_texto, anchor = "e")


    max_historial = config["dashboard"]["max_historial"]

    datos_validos = datos_validos[-max_historial:]

    horas = []
    valores = []

    for hora, valor in datos_validos:
        horas.append(hora)
        valores.append(valor)


    x_inicio = 340
    x_fin = 1080

    y_inicio = 340
    y_fin = 560

    minimo = min(valores)
    maximo = max(valores)

    if minimo == maximo:
        minimo = minimo - 1
        maximo = maximo + 1

    margen = (maximo - minimo) * 0.1

    minimo_grafica = minimo - margen
    maximo_grafica = maximo + margen


    # Ejes

    dashboard.create_line(x_inicio, y_inicio, x_inicio, y_fin, fill = color_azul_oscuro, width = 2)
    dashboard.create_line(x_inicio, y_fin, x_fin, y_fin, fill = color_azul_oscuro, width = 2)


    # Eje Y

    numero_marcas_y = 5

    for i in range(numero_marcas_y):

        proporcion = i / (numero_marcas_y - 1)

        valor_marca = maximo_grafica - proporcion * (maximo_grafica - minimo_grafica)
        y_marca = y_inicio + proporcion * (y_fin - y_inicio)

        dashboard.create_line(x_inicio - 5, y_marca, x_inicio, y_marca, fill = color_azul_oscuro)
        dashboard.create_text(x_inicio - 12, y_marca, text = str(round(valor_marca, 1)), font = fuente_pequena, fill = color_texto, anchor = "e")

    dashboard.create_text(x_inicio - 55, y_inicio - 20, text = unidades[variable_seleccionada], font = fuente_pequena, fill = color_texto)


    if len(valores) == 1:
        paso_x = 0
        x = x_fin

    else:
        paso_x = (x_fin - x_inicio) / (len(valores) - 1)
        x = x_inicio


    x_anterior = None
    y_anterior = None

    posiciones_x = []

    for valor in valores:

        y = y_fin - (valor - minimo_grafica) / (maximo_grafica - minimo_grafica) * (y_fin - y_inicio)

        if x_anterior is not None:
            dashboard.create_line(x_anterior, y_anterior, x, y, fill = color_azul_oscuro, width = 2)

        dashboard.create_oval(x - 3, y - 3, x + 3, y + 3, fill = color_azul_oscuro, outline = "")

        posiciones_x.append(x)

        x_anterior = x
        y_anterior = y

        x = x + paso_x


    # Eje X

    if len(horas) == 1:

        dashboard.create_text(x_fin, y_fin + 20, text = horas[0], font = fuente_pequena, fill = color_texto)

    else:

        indices = [0, len(horas) // 3, (len(horas) * 2) // 3, len(horas) - 1]

        indices = list(dict.fromkeys(indices))

        for indice in indices:

            x_marca = posiciones_x[indice]

            dashboard.create_line(x_marca, y_fin, x_marca, y_fin + 5, fill = color_azul_oscuro)
            dashboard.create_text(x_marca, y_fin + 20, text = horas[indice], font = fuente_pequena, fill = color_texto)


def variables(dashboard, ir_a_variable, variable_seleccionada, historial_variable, config):

    variables_fila_1 = variables_monitorizadas[:5]
    variables_fila_2 = variables_monitorizadas[5:]

    ancho_fila_1 = ancho_boton * len(variables_fila_1) + separacion_botones * (len(variables_fila_1) - 1)
    ancho_fila_2 = ancho_boton * len(variables_fila_2) + separacion_botones * (len(variables_fila_2) - 1)

    x_fila_1 = ancho_menu + (ancho_dashboard - ancho_menu - ancho_fila_1) / 2
    x_fila_2 = ancho_menu + (ancho_dashboard - ancho_menu - ancho_fila_2) / 2

    y_fila_1 = alto_cabecera + 35
    y_fila_2 = y_fila_1 + alto_boton + separacion_botones


    # Primera fila

    for i in range(len(variables_fila_1)):

        variable = variables_fila_1[i]
        x = x_fila_1 + i * (ancho_boton + separacion_botones)

        if variable == variable_seleccionada:
            color = color_azul_claro

        else:
            color = color_botones

        def seleccionar(variable_boton = variable):
            ir_a_variable(variable_boton)

        boton = tk.Button(dashboard, text = idiomas.traducir(nombres_variables[variable]), command = seleccionar, bg = color, fg = color_texto, relief = "flat", font = fuente_pequena)

        boton.place(x = x, y = y_fila_1, width = ancho_boton, height = alto_boton)


    # Segunda fila

    for i in range(len(variables_fila_2)):

        variable = variables_fila_2[i]
        x = x_fila_2 + i * (ancho_boton + separacion_botones)

        if variable == variable_seleccionada:
            color = color_azul_claro

        else:
            color = color_botones

        def seleccionar(variable_boton = variable):
            ir_a_variable(variable_boton)

        boton = tk.Button(dashboard, text = idiomas.traducir(nombres_variables[variable]), command = seleccionar, bg = color, fg = color_texto, relief = "flat", font = fuente_pequena)

        boton.place(x = x, y = y_fila_2, width = ancho_boton, height = alto_boton)


    grafica(dashboard, variable_seleccionada, historial_variable, config)