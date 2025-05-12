import abc
import json
from abc import ABC
from pathlib import Path


class FileReader:

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__file = None

    def __enter__(self):
        self.__file = open(self.__file_path, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file.close()

    def show_content(self):
        print(f"{self.__file_path} content: ")
        for line in self.__file:
            print(line, end="")

    def get_content(self):
        return self.__file.read()


class FileManager(ABC):

    def __init__(self, file_path: str):
        self.__file_path = file_path

    @property
    def file_path(self):
        return self.__file_path

    @abc.abstractmethod
    def get_content(self):
        pass

    @abc.abstractmethod
    def erase_content(self):
        pass

    @abc.abstractmethod
    def overwrite_content(self, content: str):
        pass

    @abc.abstractmethod
    def add_content(self, content: str):
        pass


class TextFileManager(FileManager):

    def get_content(self):
        with open(self.file_path) as f:
            return f.read()


    def erase_content(self):
        pass

    def overwrite_content(self, content: str):
        pass

    def add_content(self, content: str):
        pass


class BinaryFileManager(FileManager):

    def get_content(self):
        with open(self.file_path, "rb") as f:
            return f.read()

    def erase_content(self):
        pass

    def overwrite_content(self, content: str):
        pass

    def add_content(self, content: str):
        pass


class JSONFileManager(FileManager):

    def get_content(self):
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

    def erase_content(self):
        pass

    def overwrite_content(self, content: str):
        pass

    def add_content(self, content: str):
        pass

