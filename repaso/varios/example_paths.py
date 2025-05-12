from pathlib import Path


def list_directories(base_dir):
    print("# Listar directorios")
    path = Path(base_dir)
    dirs = [str(p) for p in path.iterdir() if p.is_dir()]
    print(f"Directorios: {dirs}")


def list_files(base_dir):
    print("# Listar archivos")
    path = Path(base_dir)
    files = [str(f) for f in path.iterdir() if f.is_file()]
    print(f"Archivos: {files}")


def list_scripts(base_dir):
    print("# Listar scripts: ")
    path = Path(base_dir)
    scripts = [str(s) for s in list(path.glob('**/*.py'))]
    print(f"Scripts: {scripts}")


def concatenate_paths(base_dir):
    print("# Concatenar rutas con strings")
    path = Path(base_dir)
    print(f"path ({type(path)}): {path}")
    print(f"path / 'init.d' -> {path / 'init.d'}")
    p = path / 'init.d'
    print(f"p.parts -> {p.parts}")


def show_properties():
    print(f"Existe .? {Path('.').exists()}")
    print(f"Existe temp? {Path('temp').exists()}")
    print(f"Es directorio .? {Path('.').is_dir()}")
    print(f"Es archivo .? {Path('.').is_file()}")
    print(f"Es absoluto .? {Path('.').is_absolute()}")
    print(f"Es relativo .? {Path('.').is_relative_to('.')}")


def show_file_elements(base_dir):
    p = Path(base_dir)
    print(f"p.suffix -> {p.suffix}")
    print(f"p.suffixes -> {p.suffixes}")
    print(f"p.stem -> {p.stem}")


def main():
    list_directories("../")
    breakpoint()
    list_files("../")
    breakpoint()
    list_scripts(".")
    breakpoint()
    concatenate_paths("/etc")
    breakpoint()
    show_properties()
    breakpoint()
    show_file_elements('compressed.tar.bz2')


if __name__ == "__main__":
    main()



