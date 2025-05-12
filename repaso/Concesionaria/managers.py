

class GestorVehiculos:

    def __init__(self):
        self.__vehiculos = list()

    @property
    def vehiculos(self):
        return self.__vehiculos

    def contar_vehiculos(self):
        return len(self.vehiculos)

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def dar_de_baja(self, vehiculo):
        vehiculo.marcar_como_vendido()

    def get_vehiculo(self, indice):
        return self.vehiculos[indice]

    def buscar_vehiculos(self, busqueda):
        vehiculo_encontrados = list()
        busqueda_minuscula = busqueda.lower()
        for vehiculo in self.vehiculos:
            if busqueda_minuscula in vehiculo.patente.lower() or busqueda_minuscula in vehiculo.modelo.lower() or busqueda.lower() in vehiculo.marca.lower():
                vehiculo_encontrados.append(vehiculo)

        return vehiculo_encontrados