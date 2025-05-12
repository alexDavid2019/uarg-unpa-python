from datetime import datetime
from enum import Enum, auto

class EstadoNotificacion(Enum):
    PENDIENTE = auto()
    ENTREGADO = auto()
    RECHAZO = auto()
    OTRO = auto()
    NO_ENTREGADO = auto()

class AutoridadDeMesa:
    def __init__(self, apellidos, nombres, numero_mesa, cargo, establecimiento):
        self.apellidos = apellidos
        self.nombres = nombres
        self.numero_mesa = numero_mesa
        self.cargo = cargo
        self.establecimiento = establecimiento

    def __str__(self):
        return (f"{self.apellidos}, {self.nombres} - Mesa {self.numero_mesa} "
                f"- Cargo: {self.cargo} - Establecimiento: {self.establecimiento}")

class Notificacion:
    def __init__(self, autoridad, sucursal_correo):
        self.autoridad = autoridad
        self._sucursal_correo = sucursal_correo
        self._fecha_hora = datetime.now()
        self._estado = EstadoNotificacion.PENDIENTE
        self._motivo_detalle = None

    @property
    def sucursal_correo(self):
        return self._sucursal_correo

    @property
    def fecha_hora(self):
        return self._fecha_hora.strftime("%d/%m/%Y %H:%M")

    @property
    def estado(self):
        return self._estado.name

    @estado.setter
    def estado(self, nuevo_estado):
        if isinstance(nuevo_estado, EstadoNotificacion):
            self._estado = nuevo_estado
        else:
            raise ValueError(f"Estado inválido: {nuevo_estado}.")

    @property
    def motivo_detalle(self):
        return self._motivo_detalle

    @motivo_detalle.setter
    def motivo_detalle(self, motivo):
        self._motivo_detalle = motivo.strip() if motivo else None

    def __str__(self):
        info = (
            f"{self.autoridad}\n"
            f"- Fecha y Hora: {self.fecha_hora}\n"
            f"- Estado: {self.estado}\n"
            f"- Sucursal: {self.sucursal_correo}\n"
        )
        if self._motivo_detalle:
            info += f"- Motivo: {self._motivo_detalle}\n"
        return info + "-----------------------------"

class SistemaNotificaciones:
    def __init__(self):
        self.notificaciones = []

    def agregar_notificacion(self, apellidos, nombres, numero_mesa, cargo, establecimiento, sucursal_correo):
        autoridad = AutoridadDeMesa(apellidos, nombres, numero_mesa, cargo, establecimiento)
        self.notificaciones.append(Notificacion(autoridad, sucursal_correo))

    def listar_notificaciones(self, pendientes=True):
        estado_filtro = EstadoNotificacion.PENDIENTE if pendientes else None
        ids = []
        print("# Notificaciones " + ("pendientes:" if pendientes else "procesadas:"))
        for idx, notificacion in enumerate(self.notificaciones, start=1):
            if pendientes and notificacion.estado != EstadoNotificacion.PENDIENTE.name:
                continue
            if not pendientes and notificacion.estado == EstadoNotificacion.PENDIENTE.name:
                continue
            ids.append(idx)
            print(f"{idx}\n{notificacion}")
        return ids

    def procesar(self):
        ids = self.listar_notificaciones(pendientes=True)

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

                id_para_procesar = self.seleccionar_id(ids)
                if id_para_procesar is None:
                    continue

                notificacion = self.notificaciones[id_para_procesar - 1]

                if opcion == 1:
                    notificacion.estado = EstadoNotificacion.ENTREGADO
                    print(f"Entregado a: {notificacion.autoridad}")

                elif opcion == 2:
                    self.procesar_no_entregado(notificacion)

                elif opcion == 3:
                    notificacion.estado = EstadoNotificacion.RECHAZO
                    print(f"El destinatario {notificacion.autoridad} rechazó la notificación.")

                elif opcion == 4:
                    otro_motivo = input("Ingrese el motivo: ").strip()
                    notificacion.estado = EstadoNotificacion.OTRO
                    notificacion.motivo_detalle = otro_motivo
                    print(f"Se registra otro motivo para: {notificacion.autoridad}. Motivo: {otro_motivo}")

            except ValueError:
                print("Debe ingresar un número válido.")

    def seleccionar_id(self, ids):
        while True:
            try:
                id_para_procesar = int(input("Ingrese ID a procesar o 0 para volver: "))
                if id_para_procesar == 0:
                    return None
                if id_para_procesar in ids:
                    return id_para_procesar
                print("Solo se pueden procesar los ID listados. Intente nuevamente.")
            except ValueError:
                print("Debe ingresar un número válido.")

    def procesar_no_entregado(self, notificacion):
        motivos = ["Domicilio insuficiente", "Desconocido", "Mudose", "Con Aviso"]
        while True:
            self.menu_no_entregado()
            try:
                opcion_no_entregado = int(input("Seleccione una opción: "))
                if opcion_no_entregado == 0:
                    break
                if 1 <= opcion_no_entregado <= 4:
                    notificacion.estado = EstadoNotificacion.NO_ENTREGADO
                    notificacion.motivo_detalle = motivos[opcion_no_entregado - 1]
                    print(f"Procesado como NO ENTREGADO. Motivo: {notificacion.motivo_detalle}")
                    break
                else:
                    print("Seleccione una opción válida.")
            except ValueError:
                print("Debe ingresar un número válido.")

    def menu_procesamiento(self):
        print("""
    #=========================================================#
    #           Notificaciones - Procesamiento                #  
    #=========================================================#
        1 - Entregado al destinatario
        2 - No Entregado
        3 - Rechazo
        4 - Otro
        0 - Volver
    """)

    def menu_no_entregado(self):
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

    def mostrar_menu(self):
        print("""
        1 - Crear Notificación
        2 - Procesar Notificación 
        3 - Listar Notificaciones pendientes
        4 - Listar Notificaciones No pendientes
        0 - Salir
        """)

    def iniciar(self):
        print("""
    #=========================================================#
    #           AIPython II - Sistema de Notificaciones       #  
    #=========================================================#
        """)
        self.agregar_notificacion("Morales", "Juan", 101, "Presidente de mesa", "Escuela 1", "Río Gallegos")
        self.agregar_notificacion("Toledo", "Eva", 102, "Vocal", "Escuela 2", "Caleta Olivia")

        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            if opcion == "0":
                print("Gracias por utilizar el Sistema de Notificaciones. ¡Hasta pronto!")
                break
            elif opcion == "1":
                apellidos = input("Ingrese Apellidos: ")
                nombres = input("Ingrese Nombres: ")
                numero_mesa = input("Ingrese Número de Mesa: ")
                cargo = input("Ingrese Cargo: ")
                establecimiento = input("Ingrese Establecimiento: ")
                sucursal = input("Ingrese Sucursal: ")
                self.agregar_notificacion(apellidos, nombres, numero_mesa, cargo, establecimiento, sucursal)
            elif opcion == "2":
                self.procesar()
            elif opcion == "3":
                self.listar_notificaciones(pendientes=True)
            elif opcion == "4":
                self.listar_notificaciones(pendientes=False)
            else:
                print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    sistema = SistemaNotificaciones()
    sistema.iniciar()
