"""
CONSIGNA:
    Se desea desarrollar una aplicación para una concesionaria de vehículos usados.
    Cada vehículo cuenta con la siguiente información:
    - Patente
    - Marca
    - Modelo
    - Precio
    - Año de fabricación

    Se necesita poder:
     - Cargar nuevos vehículos
     - Marcar vehículos como vendidos
     - Buscar vehículos
     - Mostrar la colección completa
    Al mostrar la colección, se debe indicar la antigüedad de cada vehículo.

    Adicionalmente, el dueño quiere poder indicar si se encuentran en oferta o no.
"""
import re
from datetime import datetime

"""
NOTAS:
- Cómo quiere navegar la información? Linea de comando
- Moneda para guardar el precio? Pesos
- Donde querés guardar la información? Lista
- Carga inicial de datos? Importación de datos?
- Modificar?

- Antigüedad la calculamos

Vehículo
- Marca: str
- Modelo: str
- Patente: str
- Precio: float
- Año de fabricación: int
- Oferta: bool
- Disponible: bool
 
 Operaciones:
 - Alta
 - Baja (marcar como vendido)
 - Buscar
 - Mostrar colección
 - Modificar
 
"""

ANIO_ACTUAL = datetime.now().year
PRICE_REGEX_VALIDATOR = r'^\d+(\.\d+)?$'


def validar_precio():
    valor_precio = input("Ingrese precio: ")
    while re.match(PRICE_REGEX_VALIDATOR, valor_precio) is None:
        valor_precio = input("Precio debe ser un decimal. Ingrese precio: ")

    precio = float(valor_precio)
    return precio


def validar_anio():
    valor_anio = input("Ingrese año: ")
    while not valor_anio.isdigit() or not len(valor_anio) == 4 or int(valor_anio) > ANIO_ACTUAL:
        valor_anio = input("Año debe ser un entero. Ingrese año: ")

    anio = int(valor_anio)

    return anio


def validar_oferta():
    valor_oferta = input("¿Está en oferta? (si/no) ")
    oferta = True if valor_oferta.lower() == "si" else False

    return oferta


def validar_disponibilidad():
    valor_disponible = input("¿Está disponible? (si/no) ")
    disponible = True if valor_disponible.lower() == "si" else False

    return disponible


def cargar_vehiculo(coleccion):
    marca = input("Ingrese marca: ")
    modelo = input("Ingrese modelo: ")
    patente = input("Ingrese patente: ")    # TODO -> Validar con REGEX

    precio = validar_precio()
    anio = validar_anio()
    oferta = validar_oferta()
    disponible = validar_disponibilidad()

    vehiculo = [marca, modelo, patente, precio, anio, oferta, disponible]

    coleccion.append(vehiculo)


def mostrar_coleccion(coleccion):
    print("# Vehículos en la colección:")
    for vehiculo in coleccion:
        marca, modelo, patente, precio, anio, oferta, disponible = vehiculo

        antiguedad = ANIO_ACTUAL - anio

        datos = f"""
        - Marca: {marca}
        - Modelo: {modelo}
        - Patente: {patente}
        - Precio: ${precio}
        - Año de fabricación: {anio}
        - Esta en oferta: {"Si" if oferta else "No"} 
        - Esta disponible: {"Si" if disponible else "No"}
        - Antigüedad: {antiguedad} años
        ----------------------------- 
        """
        print(datos)


def mostrar_menu():
    menu = '''
        1 - Alta
        2 - Baja (marcar como vendido)
        3 - Buscar
        4 - Mostrar colección
        5 - Modificar
        0 - Salir
    '''
    print(menu)


def mostrar_mensaje_de_bienvenida():
    mensaje = '''
    #=========================================================#
    #           AIPython 2 - Ejemplo 1: Concesionaria         #  
    #           -------------------------------------         #
    #=========================================================#
    '''
    print(mensaje)


def main():
    mostrar_mensaje_de_bienvenida()
    mostrar_menu()
    # coleccion = list()
    coleccion = [
        ["Ford", "Focus", "ABC 123", 11000000.0, 2014, False, True],
        ["Ford", "Fiesta", "DCE 456", 14000000.0, 2018, True, True]
    ]

    while (opcion := input("Seleccione una opción: ")) != "0":
        mostrar_menu()

        if opcion == "1":
            cargar_vehiculo(coleccion)
        elif opcion == "2":
            pass
        elif opcion == "4":
            mostrar_coleccion(coleccion)
        else:
            print("¡Ups! La opción ingresada no es válida. Intente nuevamente.")

            
    print("Gracias por utilizar la aplicación de concesionaria. ¡Vuelva pronto!")


if __name__ == '__main__':
    main()
