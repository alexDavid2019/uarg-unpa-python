from peewee import (
    SqliteDatabase, Model, IntegerField, CharField, DateField
)

DB_PATH = 'address_book.db'
db = SqliteDatabase(DB_PATH, pragmas={'journal_mode': 'wal'})


class Contact(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=64, null=False)
    last_name = CharField(max_length=64, null=False)
    phone = CharField(max_length=16, null=True)
    email = CharField(max_length=64, null=True)
    birthday = DateField(null=True)

    class Meta:
        database = db
        table_name = 'contact'


def create_address_book():
    """
    Crea la tabla contact en la base de datos si no existe.
    """
    try:
        db.create_tables([Contact])
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
        birthday (str): Fecha de nacimiento del contacto (formato 'YYYY-MM-DD').
    """
    try:
        Contact.create(
            name=name,
            last_name=last_name,
            phone=phone,
            email=email,
            birthday=birthday
        )
    except Exception as e:
        print(f"Ha ocurrido un error al agregar un contacto: {e}")


def delete_contact(contact_id):
    """
    Elimina un contacto de la base de datos.

    Args:
        contact_id (int): ID del contacto a eliminar.
    """
    try:
        contact = Contact.get_or_none(Contact.id == contact_id)
        if contact:
            contact.delete_instance()
        else:
            print(f"No se encontró un contacto con ID {contact_id}")
    except Exception as e:
        print(f"Ha ocurrido un error al eliminar un contacto: {e}")


def update_contact(contact_id, name, last_name, phone, email, birthday):
    """
    Modifica los datos de un contacto existente en la base de datos.

    Args:
        contact_id (int): ID del contacto a modificar.
        name (str): Nuevo nombre del contacto.
        last_name (str): Nuevo apellido del contacto.
        phone (str): Nuevo teléfono del contacto.
        email (str): Nuevo correo electrónico del contacto.
        birthday (str): Nueva fecha de nacimiento del contacto (formato 'YYYY-MM-DD').
    """
    try:
        contact = Contact.get_or_none(Contact.id == contact_id)
        if contact:
            contact.name = name
            contact.last_name = last_name
            contact.phone = phone
            contact.email = email
            contact.birthday = birthday
            contact.save()
        else:
            print(f"No se encontró un contacto con ID {contact_id}")
    except Exception as e:
        print(f"Ha ocurrido un error al modificar un contacto: {e}")


def search_contact(contact_id):
    """
    Busca un contacto en la base de datos por su ID.

    Args:
        contact_id (int): ID del contacto a buscar.

    Returns:
        result: Tupla con los datos del contacto (id, name, last_name, phone, email, birthday) o None si no se encuentra.
    """
    result = None
    try:
        contact = Contact.get_or_none(Contact.id == contact_id)
        if contact:
            result = contact.id, contact.name, contact.last_name, contact.phone, contact.email, contact.birthday
    except Exception as e:
        print(f"Ha ocurrido un error al buscar un contacto: {e}")
    return result


def get_contact_list():
    """
    Recupera la lista completa de contactos de la base de datos.

    Returns:
        list: Lista de tuplas, cada una con los datos de un contacto (id, name, last_name, phone, email, birthday).
    """
    try:
        contacts = Contact.select().order_by(Contact.id.asc())
        return [(c.id, c.name, c.last_name, c.phone, c.email, c.birthday) for c in contacts]
    except Exception as e:
        print(f"Ha ocurrido un error al obtener la lista de contactos: {e}")
        return []


def main():
    create_address_book()
    insert_contact("Pepe", "Gomez", "123-456-789", "pepe@gomez.com", "1990-01-01")
    contacts = get_contact_list()
    if contacts:
        for contact in contacts:
             print(contact)
    else:
        print("No hay contactos cargados en la base")


if __name__ == "__main__":
    main()