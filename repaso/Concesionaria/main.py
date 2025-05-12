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

import sys
from ui import CLInterface



def main():
    interfaz = CLInterface()
    interfaz.mostrar_mensaje_de_bienvenida()
    interfaz.ejecutar()
    interfaz.mostrar_mensaje_de_despedida()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Saliendo de aplicación AIPython II - Concesionaria")
        sys.exit(0)
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
        sys.exit(1)

