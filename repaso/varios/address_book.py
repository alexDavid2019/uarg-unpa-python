import sqlite3
from queries import (
    ADDRESS_BOOK_CREATE_SQL, ADDRESS_BOOK_INSERT_SQL, ADDRESS_BOOK_DELETE_SQL,
    ADDRESS_BOOK_UPDATE_SQL, ADDRESS_BOOK_SELECT_SQL, ADDRESS_BOOK_SELECT_ALL_SQL
)

DB_PATH = 'address_book.db'


def get_connection():
    """
    Establecer conexión a la base de datos en la ruta indicada.
    En caso de que no exista, crearla y establecer la conexión.
    """
    return sqlite3.connect(DB_PATH)


def create_address_book():
    """
    Crea la tabla contact si no existe con los campos:
    - id (autoincremental)
    - name: tipo de variable str
    - last_name: tipo de variable str
    - phone: tipo de variable str (para contemplar espacios y guiones)
    - email: tipo de variable str
    - birthday: tipo de variable date
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ADDRESS_BOOK_CREATE_SQL)
            conn.commit()
    except Exception as e:
        print(f"Ha ocurrido un error al crear la tabla contact: {e}")


def insert_contact(name, last_name, phone, email, birthday):
    """
    Agrega un nuevo contacto a la base de datos.

    Args:
        name (str): Nombre del contacto.
        last_name (str): Apellido del contacto.
        phone (str): Teléfono del contacto.
        email (str): Correo electrónico del contacto.
        birthday (str): Fecha de nacimiento del contacto.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                ADDRESS_BOOK_INSERT_SQL,
                (name, last_name, phone, email, birthday)
            )
            conn.commit()
    except Exception as e:
        print(f"Ha ocurrido un error al agregar contacto a la base de datos: {e}")


def delete_contact(contact_id):
    """
    Elimina un contacto de la base de datos.

    Args:
        contact_id (int): ID del contacto a eliminar.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ADDRESS_BOOK_DELETE_SQL, (contact_id,))
            conn.commit()
    except Exception as e:
        print(f"Ha ocurrido un error al eliminar contacto de la base de datos: {e}")


def update_contact(contact_id, name, last_name, phone, email, birthday):
    """
    Modifica un contacto en la base de datos.

    Args:
        contact_id (int): ID del contacto a modificar.
        name (str): Nuevo nombre del contacto.
        last_name (str): Nuevo apellido del contacto.
        phone (str): Nuevo teléfono del contacto.
        email (str): Nuevo correo electrónico del contacto.
        birthday (str): Nueva fecha de nacimiento del contacto.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                ADDRESS_BOOK_UPDATE_SQL,
                (name, last_name, phone, email, birthday, contact_id)
            )
            conn.commit()
    except Exception as e:
        print(f"Ha ocurrido un error al modificar contacto: {e}")


def search_contact(contact_id):
    """
    Busca un contacto en la base de datos.

    Args:
        contact_id (int): ID del contacto a buscar.

    Returns:
        tuple: Tupla con los datos del contacto o None si no se encuentra.
    """
    result = None
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ADDRESS_BOOK_SELECT_SQL, (contact_id,))
            result = cursor.fetchone()
    except Exception as e:
        print(f"Ha ocurrido un error al buscar contacto en la base de datos: {e}")

    return result


def get_contact_list():
    """
    Recupera toda la lista de contactos de la base de datos.

    Returns:
        list: Lista de tuplas con los datos de los contactos.
    """
    result = []
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ADDRESS_BOOK_SELECT_ALL_SQL)
            result = cursor.fetchall()
    except Exception as e:
        print(f"Ha ocurrido un error al obtener la lista de contactos de la base de datos: {e}")

    return result


def main():
    create_address_book()
    insert_contact("Juanita", "Lopez", "432-654-321", "juanita@lopez.com", "2000-01-01")
    contacts = get_contact_list()
    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No hay contactos cargados en la base")


if __name__ == "__main__":
    main()