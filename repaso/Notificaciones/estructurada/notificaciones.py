from datetime import datetime

def crear_notificacion(apellidos, nombres, sucursal_correo):
    return [
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

def agregar_notificacion(notificaciones, apellidos, nombres, sucursal_correo):
    notificacion = crear_notificacion(apellidos, nombres, sucursal_correo)
    notificaciones.append(notificacion)

def listar_pendientes(coleccion):
    print("# Notificaciones pendientes:")
    ids = ()
    for idx, notificacion in enumerate(coleccion, start=1):
        apellidos, nombres, fecha_hora, estado, sucursal_correo = notificacion
        if estado == "PENDIENTE":
            ids += (idx,)
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

def menu_procesamiento():
    menu = """
    #=========================================================#
    #           Notificaciones - Procesamiento                #  
    #           -------------------------------------         #
    #=========================================================#
        1 - Entregado al remitente (PROCESADO)
        2 - No Entregado
        3 - Rechazo
        4 - Otro
        0 - Volver
    """
    print(menu)

def menu_no_entregado():
    menu = """
    #=========================================================#
    #           Notificaciones - NO ENTREGADAS                #  
    #           -------------------------------------         #
    #=========================================================#
        1 - Domicilio insuficiente
        2 - Desconocido
        3 - Mudose
        4 - Con Aviso
        0 - Volver
    """
    print(menu)

def procesar(coleccion):
    ids = listar_pendientes(coleccion)
    menu_procesamiento()
    while (opcion := int(input("Seleccione una opción o 0 para volver: "))) != 0:
        while (id_para_procesar := int(input("Ingrese ID a procesar o 0 para volver: "))) not in ids:
            if id_para_procesar == 0:
                opcion = 0
                break
            print("Solo se pueden procesar los ID listados")
            print(ids)
            print("Volver, presione: 0")
        if opcion == 0:
            break
        if opcion == 1:
            coleccion[id_para_procesar - 1][3] = "PROCESADO"
            print(f"Entregado a: {coleccion[id_para_procesar - 1][0]}, {coleccion[id_para_procesar - 1][1]}, Procesado")
        elif opcion == 2:
            menu_no_entregado()
            while (opcion_no_entregado := int(input("Seleccione una opción: "))) not in range(0, 6):
                print("Seleccione una opción válida")
                menu_no_entregado()
            motivos = [
                "Domicilio insuficiente",
                "Desconocido",
                "Mudose",
                "Con Aviso",
            ]
            if 1 <= opcion_no_entregado <= 4:
                coleccion[id_para_procesar - 1][3] = motivos[opcion_no_entregado - 1]
                print("Procesado con éxito")
            else:
                print("Volviendo, seleccionó una opción no válida. Intente nuevamente.")
                break
        elif opcion == 3:
            coleccion[id_para_procesar - 1][3] = "RECHAZADO"
            print(f"El destinatario: {coleccion[id_para_procesar - 1][0]}, {coleccion[id_para_procesar - 1][1]}, Rechazo la notificacion")
        elif opcion == 4:
            otro_motivo=input("Ingrese el motivo: ")
            coleccion[id_para_procesar - 1][3] = f"OTRO - {otro_motivo}"
            print(f"Se registra otro motivo para el destinatario: {coleccion[id_para_procesar - 1][0]}, {coleccion[id_para_procesar - 1][1]}")
        else:
            print("¡Ups! La opción ingresada no es válida. Intente nuevamente.")
        menu_procesamiento()
    

def mostrar_menu():
    menu = """
        1 - Crear Notificación
        2 - Procesar por número de notificación 
        3 - Listar Notificaciones pendientes
        0 - Salir
    """
    print(menu)

def mostrar_mensaje_de_bienvenida():
    mensaje = """
    #=========================================================#
    #           AIPython II - Ejemplo x: Notificaciones       #  
    #           -------------------------------------         #
    #=========================================================#
    """
    print(mensaje)

def main():
    mostrar_mensaje_de_bienvenida()
    mostrar_menu()
    notificaciones = []
    
    # Agregar notificaciones de prueba con datos de Santa Cruz, Argentina
    agregar_notificacion(notificaciones, "Pérez", "Juan", "Río Gallegos")
    agregar_notificacion(notificaciones, "Gómez", "María", "Caleta Olivia")
    agregar_notificacion(notificaciones, "Fernández", "Carlos", "Pico Truncado")
    agregar_notificacion(notificaciones, "López", "Ana", "Puerto Deseado")
    
    while (opcion := input("Seleccione una opción: ")) != "0":
        if opcion == "1":
            nombres = input("Ingrese Nombres: ")
            apellidos = input("Ingrese Apellidos: ")
            sucursal = input("Ingrese Sucursal: ")
            agregar_notificacion(notificaciones, nombres, apellidos, sucursal)
        elif opcion == "2":
            procesar(notificaciones)
        elif opcion == "3":
            listar_pendientes(notificaciones)
        else:
            print("¡Ups! La opción ingresada no es válida. Intente nuevamente.")
        mostrar_menu()
    print("Gracias por utilizar la aplicación de Notificaciones. ¡Vuelva pronto!")

if __name__ == "__main__":
    main()
