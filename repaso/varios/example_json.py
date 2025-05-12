import json
from pathlib import Path


class JSONStorage:

    def __init__(self, file_path: str):
        self.__file_path = file_path

    @property
    def file_path(self):
        return self.__file_path

    def save_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        data = {}
        file = Path(self.file_path)
        if file.exists():
            with open(self.file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error al abrir archivo JSON: {e}")
        else:
            print(f"No hay archivo de datos. Creando uno vacío.")
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
        
        return data


if __name__ == "__main__":
    archivo = "example/prueba.json"
    storage = JSONStorage(archivo)
    data = {
        "k1": 1,
        "k2": "string",
        "k3": 3.1,
        "k4": True
    }
    storage.save_data(data)
    data = storage.load_data()
    print(f"data: {data}")
