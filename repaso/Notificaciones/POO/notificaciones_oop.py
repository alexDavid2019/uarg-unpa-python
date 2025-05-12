from datetime import datetime

class Notificacion:
    def __init__(self, apellidos, nombres, sucursal_correo):
        self.apellidos = apellidos
        self.nombres = nombres
        self.sucursal_correo = sucursal_correo
        self.fecha_hora = (
            datetime.now().day, datetime.now().month, datetime.now().year,
            datetime.now().hour, datetime.now().minute
        )
        self.estado = "PENDIENTE"

    def procesar(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return (f"- Apellidos: {self.apellidos}\n"
                f"- Nombres: {self.nombres}\n"
                f"- Fecha: {'/'.join(map(str, self.fecha_hora[:3]))}\n"
                f"- Hora: {self.fecha_hora[3]:02}:{self.fecha_hora[4]:02}\n"
                f"- Estado: {self.estado}\n"
                f"- Sucursal: {self.sucursal_correo}\n"
                "-----------------------------")


class SistemaNotificaciones:
    def __init__(self):
        """Inicializa el sistema con una lista de notificaciones vacía."""
        self.notificaciones = []

    def agregar_notificacion(self, apellidos, nombres, sucursal_correo):
        """Agrega una nueva notificación a la lista."""
        notificacion = [
            apellidos,
            nombres,
            (
                datetime.now().day,
                datetime.now().month,
                datetime.now().year,
                datetime.now().hour,
                datetime.now().minute,
            ),
            "PENDIENTE",
            sucursal_correo,
        ]
        self.notificaciones.append(notificacion)

    def listar_pendientes(self):
        """Lista todas las notificaciones pendientes y devuelve sus IDs."""
        print("# Notificaciones pendientes:")
        ids = []
        for idx, notificacion in enumerate(self.notificaciones, start=1):
            apellidos, nombres, fecha_hora, estado, sucursal_correo = notificacion
            if estado == "PENDIENTE":
                ids.append(idx)
                datos = (
                    f"{idx}\n"
                    f"- Apellidos: {apellidos}\n"
                    f"- Nombres: {nombres}\n"
                    f"- Fecha: {'/'.join(map(str, fecha_hora[:3]))}\n"
                    f"- Hora: {fecha_hora[3]}:{fecha_hora[4]}\n"
                    f"- Estado: {estado}\n"
                    f"- Sucursal: {sucursal_correo}\n"
                    "-----------------------------"
                )
                print(datos)
        return ids

    def listar_no_pendientes(self):
        """Lista todas las notificaciones pendientes y devuelve sus IDs."""
        print("# Notificaciones pendientes:")
        ids = []
        for idx, notificacion in enumerate(self.notificaciones, start=1):
            apellidos, nombres, fecha_hora, estado, sucursal_correo = notificacion
            if estado != "PENDIENTE":
                ids.append(idx)
                datos = (
                    f"{idx}\n"
                    f"- Apellidos: {apellidos}\n"
                    f"- Nombres: {nombres}\n"
                    f"- Fecha: {'/'.join(map(str, fecha_hora[:3]))}\n"
                    f"- Hora: {fecha_hora[3]}:{fecha_hora[4]}\n"
                    f"- Estado: {estado}\n"
                    f"- Sucursal: {sucursal_correo}\n"
                    "-----------------------------"
                )
                print(datos)

    def menu_procesamiento(self):
        """Muestra el menú de procesamiento de notificaciones."""
        print("""
    #=========================================================#
    #           Notificaciones - Procesamiento                #  
    #=========================================================#
        1 - Entregado al remitente (PROCESADO)
        2 - No Entregado
        3 - Rechazo
        4 - Otro
        0 - Volver
    """)

    def menu_no_entregado(self):
        """Muestra el menú para seleccionar motivo de no entrega."""
        print("""
    #=========================================================#
    #           Notificaciones - NO ENTREGADAS                #  
    #=========================================================#
        1 - Domicilio insuficiente
        2 - Desconocido
        3 - Mudose
        4 - Con Aviso
        0 - Volver
    """)

    def procesar(self):
        """Permite procesar notificaciones en base a un menú de opciones."""
        ids = self.listar_pendientes()

        if not ids:
            print("No hay notificaciones pendientes para procesar.")
            return

        while True:
            self.menu_procesamiento()
            try:
                opcion = int(input("Seleccione una opción o 0 para volver: "))
                if opcion == 0:
                    break
                if opcion not in [1, 2, 3, 4]:
                    print("Opción inválida, intente nuevamente.")
                    continue

                while True:
                    try:
                        id_para_procesar = int(input("Ingrese ID a procesar o 0 para volver: "))
                        if id_para_procesar == 0:
                            break
                        if id_para_procesar in ids:
                            break
                        print("Solo se pueden procesar los ID listados. Intente nuevamente.")
                    except ValueError:
                        print("Debe ingresar un número válido.")

                if id_para_procesar == 0:
                    continue

                notificacion = self.notificaciones[id_para_procesar - 1]

                if opcion == 1:
                    notificacion[3] = "PROCESADO"
                    print(f"Entregado a: {notificacion[0]}, {notificacion[1]}, Procesado")

                elif opcion == 2:
                    while True:
                        self.menu_no_entregado()
                        try:
                            opcion_no_entregado = int(input("Seleccione una opción: "))
                            if opcion_no_entregado == 0:
                                break
                            motivos = ["Domicilio insuficiente", "Desconocido", "Mudose", "Con Aviso"]
                            if 1 <= opcion_no_entregado <= 4:
                                notificacion[3] = motivos[opcion_no_entregado - 1]
                                print("Procesado con éxito")
                                break
                            else:
                                print("Seleccione una opción válida.")
                        except ValueError:
                            print("Debe ingresar un número válido.")

                elif opcion == 3:
                    notificacion[3] = "RECHAZADO"
                    print(f"El destinatario {notificacion[0]}, {notificacion[1]} rechazó la notificación.")

                elif opcion == 4:
                    otro_motivo = input("Ingrese el motivo: ").strip()
                    notificacion[3] = f"OTRO - {otro_motivo}"
                    print(f"Se registra otro motivo para el destinatario: {notificacion[0]}, {notificacion[1]}.")

            except ValueError:
                print("Debe ingresar un número válido.")

    def mostrar_menu(self):
        """Muestra el menú principal del sistema."""
        print("""
        1 - Crear Notificación
        2 - Procesar por número de notificación 
        3 - Listar Notificaciones pendientes
        4 - Listar Notificaciones No pendientes
        0 - Salir
        """)

    def mostrar_mensaje_de_bienvenida(self):
        """Muestra un mensaje de bienvenida."""
        print("""
    #=========================================================#
    #           AIPython II - Sistema de Notificaciones       #  
    #=========================================================#
        """)

    def iniciar(self):
        """Método principal para ejecutar el sistema."""
        self.mostrar_mensaje_de_bienvenida()
        self.mostrar_menu()

        # Agregar notificaciones de prueba con datos de Santa Cruz, Argentina
        self.agregar_notificacion("Pérez", "Juan", "Río Gallegos")
        self.agregar_notificacion("Gómez", "María", "Caleta Olivia")
        self.agregar_notificacion("Fernández", "Carlos", "Pico Truncado")
        self.agregar_notificacion("López", "Ana", "Puerto Deseado")

        while True:
            opcion = input("Seleccione una opción: ")
            if opcion == "0":
                print("Gracias por utilizar el Sistema de Notificaciones. ¡Hasta pronto!")
                break
            elif opcion == "1":
                nombres = input("Ingrese Nombres: ")
                apellidos = input("Ingrese Apellidos: ")
                sucursal = input("Ingrese Sucursal: ")
                self.agregar_notificacion(apellidos, nombres, sucursal)
            elif opcion == "2":
                self.procesar()
            elif opcion == "3":
                self.listar_pendientes()
            elif opcion == "4":
                self.listar_no_pendientes()
            else:
                print("¡Ups! La opción ingresada no es válida. Intente nuevamente.")

            self.mostrar_menu()


# Ejecución del sistema
if __name__ == "__main__":
    sistema = SistemaNotificaciones()
    sistema.iniciar()
