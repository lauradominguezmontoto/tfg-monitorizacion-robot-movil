
def seleccionar_modo():

    while True:
        print("\nSeleccione el modo de funcionamiento:")
        print("1. Modo simulado")
        print("2. Modo físico")
        print("3. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            return "simulado"

        elif opcion == "2":
            return "fisico"

        elif opcion == "3":
            return None

        else:
            print("Escriba 1, 2 o 3.")