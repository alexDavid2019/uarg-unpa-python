import re
from datetime import datetime

from managers import GestorVehiculos
from models import Vehiculo


ANIO_ACTUAL = datetime.now().year
PRECIO_REGEX_VALIDATOR = r'^\d+(\.\d+)?$'
PATENTE_REGEX_VALIDATOR = r'^[A-Z]{2,3}\s\d{3}(?:\s[A-Z]{2})?$'


class CLInterface:

    def __init__(self):
        self.__gestor = GestorVehiculos()
        self.popular_lista()

    @property
    def gestor(self):
        return self.__gestor

    def popular_lista(self):
        self.__gestor.agregar_vehiculo(Vehiculo("Ford", "Focus", "ABC 123", 11000000.0, 2014, False, True))
        self.__gestor.agregar_vehiculo(Vehiculo("Ford", "Fiesta", "DCE 456", 14000000.0, 2018, True, True))

    def mostrar_menu(self):
        menu = '''
            1 - Alta
            2 - Baja (marcar como vendido)
            3 - Buscar
            4 - Mostrar colección
            5 - Modificar
            0 - Salir
        '''
        print(menu)

    def mostrar_mensaje_de_bienvenida(self):
        mensaje = '''
        #=========================================================#
        #           AIPython 2 - Ejemplo 1: Concesionaria         #  
        #           -------------------------------------         #
        #=========================================================#
        '''
        print(mensaje)

    def mostrar_mensaje_de_despedida(self):
        print("Gracias por utilizar la aplicación de concesionaria. ¡Vuelva pronto!")

    def ejecutar(self):
        self.mostrar_menu()
        while (opcion := input("Seleccione una opción: ")) != "0":
            if opcion == "1":
                self.cargar_vehiculo()
            elif opcion == "2":
                self.dar_de_baja()
            elif opcion == "3":
                self.buscar_vehiculo()
            elif opcion == "4":
                self.mostrar_coleccion()
            else:
                print("¡Ups! La opción ingresada no es válida. Intente nuevamente.")

            self.mostrar_menu()

    def validar_marca(self):
        marca = input("Ingrese marca: ")
        while marca is None:
            marca = input("Marca no puede estar vacío. Ingrese marca: ")

        return marca

    def validar_modelo(self):
        modelo = input("Ingrese modelo: ")
        while modelo is None:
            modelo = input("Modelo no puede estar vacío. Ingrese modelo: ")

        return modelo

    def validar_patente(self):
        patente = input("Ingrese patente: ")
        while re.match(PATENTE_REGEX_VALIDATOR, patente) is None:
            patente = input("Patente debe respetar el formato ABC 123 o AB 123 CD. Ingrese patente: ")

        return patente

    def validar_precio(self):
        valor_precio = input("Ingrese precio: ")
        while re.match(PRECIO_REGEX_VALIDATOR, valor_precio) is None:
            valor_precio = input("Precio debe ser un decimal. Ingrese precio: ")

        precio = float(valor_precio)
        return precio

    def validar_anio(self):
        valor_anio = input("Ingrese año: ")
        while not valor_anio.isdigit() or not len(valor_anio) == 4 or int(valor_anio) > ANIO_ACTUAL:
            valor_anio = input("Año debe ser un entero. Ingrese año: ")

        anio = int(valor_anio)

        return anio

    def validar_oferta(self):
        valor_oferta = input("¿Está en oferta? (si/no) ")
        oferta = True if valor_oferta.lower() == "si" else False

        return oferta

    def validar_disponibilidad(self):
        valor_disponible = input("¿Está disponible? (si/no) ")
        disponible = True if valor_disponible.lower() == "si" else False

        return disponible

    def cargar_vehiculo(self):
        marca = self.validar_marca()
        modelo = self.validar_modelo()
        patente = self.validar_patente()
        precio = self.validar_precio()
        anio = self.validar_anio()
        oferta = self.validar_oferta()
        disponible = self.validar_disponibilidad()

        vehiculo = Vehiculo(marca, modelo, patente, precio, anio, oferta, disponible)

        self.gestor.agregar_vehiculo(vehiculo)

    def dar_de_baja(self):
        self.mostrar_coleccion()
        valor_vehiculo_seleccionado = input("Seleccione el vehículo a dar de baja: ")
        while not str(valor_vehiculo_seleccionado).isdigit() or int(valor_vehiculo_seleccionado) < 0 or int(valor_vehiculo_seleccionado) > self.gestor.contar_vehiculos():
            valor_vehiculo_seleccionado = input(
                "Debe seleccionar uno de los vehículos en la lista. Ingrese un número: ")

        indice_vehiculo_seleccionado = int(valor_vehiculo_seleccionado)

        vehiculo_seleccionado = self.gestor.get_vehiculo(indice_vehiculo_seleccionado)
        self.gestor.dar_de_baja(vehiculo_seleccionado)

        print(f"El vehículo se ha dado de baja con éxito")

    def buscar_vehiculo(self):
        busqueda = input("Ingrese un valor a buscar (modelo, marca o patente): ")
        vehiculos_encontrados = self.gestor.buscar_vehiculos(busqueda)

        if vehiculos_encontrados:
            print(f"Resultado de búsqueda:")
            for v in vehiculos_encontrados:
                self.mostrar_vehiculo(v)
        else:
            print(f"No se han encontrado resultados para su búsqueda.")

    def mostrar_vehiculo(self, vehiculo):
        print(vehiculo)

    def mostrar_coleccion(self):
        print("# Vehículos en la colección:")
        for i, vehiculo in enumerate(self.gestor.vehiculos):
            print(f"# {i}")
            self.mostrar_vehiculo(vehiculo)


