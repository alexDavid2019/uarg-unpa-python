"""
Recomendaciones para el orden de importacion:
"""
#1. Librerias standard
import os
#2. Librerias de terceros

#3. Librerias propias

def writeFile(path, content):
    """
    Writes a file.

    :param path: Path to the file.
    :param content: Message to write.
    """
    old_umask = os.umask(0o077)
    try:
        with open(path, "wb") as f:
            f.write(content)
    finally:
        os.umask(old_umask)


def cleanFolderForFile(filepath):
    """
    Makes sure the folder exists for a given file and that the file doesn't exist.

    :param filepath: Path to the file we want to make sure the parent directory
                        exists.
    """
    if os.path.exists(filepath):
        os.remove(filepath)

