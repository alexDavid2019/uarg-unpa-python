from datetime import datetime

ANIO_ACTUAL = datetime.now().year

class Vehiculo:

    def __init__(
            self,
            marca,
            modelo,
            patente,
            precio,
            anio,
            oferta,
            disponible
    ):
        self.__marca = marca
        self.__modelo = modelo
        self.__patente = patente
        self.__precio = precio
        self.__anio = anio
        self.__oferta = oferta
        self.__disponible = disponible

    @property
    def marca(self):
        return self.__marca

    @property
    def modelo(self):
        return self.__modelo

    @property
    def patente(self):
        return self.__patente

    @property
    def precio(self):
        return self.__precio

    @property
    def anio(self):
        return self.__anio

    @property
    def oferta(self):
        return self.__oferta

    @property
    def disponible(self):
        return self.__disponible

    def marcar_como_vendido(self):
        self.__disponible = False

    def __eq__(self, vehiculo):
        iguales = False
        if (
            self.__marca == vehiculo.marca and
            self.__modelo == vehiculo.modelo and
            self.__patente == vehiculo.patente and
            self.__precio == vehiculo.precio and
            self.__anio == vehiculo.anio and
            self.__oferta == vehiculo.oferta and
            self.__disponible == vehiculo.disponible
        ):
            iguales = True

        return iguales

    def __str__(self):
        antiguedad = ANIO_ACTUAL - self.__anio
        return f"""
        - Marca: {self.__marca}
        - Modelo: {self.__modelo}
        - Patente: {self.__patente}
        - Precio: ${self.__precio}
        - Año de fabricación: {self.__anio}
        - Esta en oferta: {"Si" if self.__oferta else "No"} 
        - Esta disponible: {"Si" if self.__disponible else "No"}
        - Antigüedad: {antiguedad} años
        ----------------------------- 
        """

if __name__ == "__main__":
    vehiculo1 = Vehiculo("Toyota", "Corolla", "ABC 123", 15000, 2020, False, True)
    vehiculo2 = Vehiculo("Toyota", "Corolla", "ABC 123", 15000, 2020, False, True)
    vehiculo3 = Vehiculo("Ford", "Focus", "XYZ 789", 12000, 2018, True, False)
    print(vehiculo1 == vehiculo2)
    print(vehiculo1 == vehiculo3)
    print(vehiculo2 == vehiculo3)