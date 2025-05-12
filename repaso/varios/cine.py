import sqlite3


CINE_DB = "cine.db"
NAME, RELEASE_DATE, CATEGORY = range(3)


def initialize_database(db_filename: str = CINE_DB):
    conn = None
    try:
        conn = sqlite3.connect(db_filename)
        print(f"SQLite version: {sqlite3.sqlite_version}")
    except sqlite3.Error as e:
        print(f"Error al crear base de datos: {e}")
    finally:
        if conn:
            conn.close()


def create_tables():
    create_pelicula_statement = """
    CREATE TABLE IF NOT EXISTS pelicula (
        id INTEGER PRIMARY KEY,
        name text NOT NULL,
        release_date DATE,
        category TEXT
    )
    """
    try:
        with sqlite3.connect(CINE_DB) as conn:
            cur = conn.cursor()
            cur.execute(create_pelicula_statement)

            conn.commit()
    except sqlite3.Error as e:
        print(f"Error al inicializar tablas: {e}")


def populate_database():
    peliculas = [
        ("The Shawshank Redemption", "1994-09-23", "Drama"),
        ("The Godfather", "1972-03-15", "Crime"),
        ("The Dark Knight", "2008-07-18", "Action"),
        ("Pulp Fiction", "1994-10-14", "Crime"),
        ("The Lord of the Rings: The Fellowship of the Ring", "2001-12-19", "Fantasy"),
        ("Forrest Gump", "1994-07-06", "Drama"),
        ("Inception", "2010-07-16", "Sci-Fi"),
        ("The Matrix", "1999-03-31", "Sci-Fi"),
        ("Good Will Hunting", "1997-12-05", "Drama"),
        ("Star Wars: Episode IV - A New Hope", "1977-05-25", "Sci-Fi")
    ]
    
    print("Cargando películas en la base de datos...")
    
    for pelicula in peliculas:
        try:
            pelicula_cargada = search_by_name(pelicula[NAME])
            if not pelicula_cargada:
                add_pelicula(*pelicula)
                print(f"Película agregada: {pelicula[NAME]}")
            else:
                print(f"La película ya está cargada: {pelicula_cargada}")
        except sqlite3.Error as e:
            print(f"Error agregando {pelicula[NAME]}: {e}")


def get_connection(db_filename: str = CINE_DB):
    conn = sqlite3.connect(db_filename)
    return conn


def add_pelicula(name, release_date, category):
    sql = """INSERT INTO pelicula(name, release_date, category) VALUES (?, ?, ?)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (name, release_date, category))
    conn.commit()
    conn.close()


def search_by_name(name):
    sql = """SELECT * from pelicula where name = ?"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (name, ))
        row = cur.fetchone()

    except sqlite3.Error as e:
        print(f"Error al buscar película por nombre: {e}")
    finally:
        if conn:
            conn.close()

        return row


def search_all():
    conn = None
    sql = """SELECT * from pelicula"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

    except sqlite3.Error as e:
        print(f"Error al buscar películas: {e}")
    finally:
        if conn:
            conn.close()

        return rows


def show_movies():
    peliculas = search_all()
    for pelicula in peliculas:
        movie_id, name, release_date, category = pelicula
        movie_data = {
            'id': movie_id,
            'name': name,
            'release_date': release_date,
            'category': category
        }
        print("-----------------------")
        for k, v in movie_data.items():
            print(f"{k.upper()}: {v}")


def main():
    initialize_database()
    create_tables()
    populate_database()
    show_movies()


if __name__ == "__main__":
    main()