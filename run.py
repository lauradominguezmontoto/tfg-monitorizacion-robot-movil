from src.monitorizacion_robot import menu_modo
from src.monitorizacion_robot import sistema_principal


while True:

    modo = menu_modo.seleccionar_modo()

    if modo is None:
        print("\nSistema cerrado.")
        break

    try:
        sistema_principal.main(modo)

    except KeyboardInterrupt:
        print("\nVolviendo al menú...")