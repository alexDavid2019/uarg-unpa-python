

TEXT_FILE = "sample.txt"


def write_to_file():
    print("\n# Escribir archivo: ")
    text = input("Ingrese un texto: ")

    f = open(TEXT_FILE, 'w', encoding="utf-8")
    f.write(f"{text}\n")
    f.close()


def read_from_file():
    print("\n# Leer archivo: ")
    with open(TEXT_FILE, 'r') as f:
        text = f.read()

    print(f"Contenido de archivo: \n{text}")


def navigate_file():
    print("\n# Navegar archivo: ")
    with open(TEXT_FILE, 'rb') as f:
        print("f.seek(3)")
        f.seek(3)
        print(f"f.read(): {f.read()}")
        print("f.seek(-2, 2)")
        f.seek(-2, 2)
        print(f"f.read(): {f.read()}")
        print("f.seek(0)")
        f.seek(0)
        print(f"f.read(4): {f.read(4)}")
        print(f"f.tell(): {f.tell()}")
        

def append_to_file():
    print("\n# Agregar a archivo: ")
    with open(TEXT_FILE, 'a') as f:
        while (text := input("Ingrese una linea: ")) != "0":
            f.write(f"{text}\n")

def read_by_line():
    print("\n# Leer línea por línea: ")
    with open(TEXT_FILE, 'r+') as f:
        for line in f:
            print(line, end='')



class MiErrorPersonalizado(ValueError):
    pass


def open_missing_file():
    try:
        with open('missing.txt', 'r') as f:
            print(f"{f.read()}")
    except FileNotFoundError as e:
        print(f"¡No he visto ese archivo en mi vida! -> {e}")
    except Exception as e:
        print("Otro error")
    else:
        print("HOLA")
    finally:
        print("FIN")
        raise MiErrorPersonalizado("Ejemplo de excepcion personalizada")


def main():
    write_to_file()
    breakpoint()
    read_from_file()
    breakpoint()
    navigate_file()
    breakpoint()
    append_to_file()
    breakpoint()
    read_by_line()
    breakpoint()
    open_missing_file()

if __name__ == "__main__":
    main()
