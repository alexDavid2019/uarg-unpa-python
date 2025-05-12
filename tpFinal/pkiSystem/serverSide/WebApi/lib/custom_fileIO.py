"""
Recomendaciones para el orden de importacion:
"""
#1. Librerias standard
import sys
import os
import csv
import datetime
import hashlib
import base64

#2. Librerias de terceros
from OpenSSL import crypto
from cryptography.hazmat.primitives.serialization import pkcs12

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

def get_files_recursive(target_dir) -> list:
    file_list = list()
    #onlyFiles = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    item_list = os.listdir(target_dir)
    for item in item_list:
        item_dir = os.path.join(target_dir,item)
        if os.path.isdir(item_dir):
            file_list += get_files_recursive(item_dir)
        else:
            file_list.append(item_dir)
    return file_list

def get_files_recursive_metadata(target_dir) -> dict:
    #dictionary
    recursiveDict = {}
    
    item_list = os.listdir(target_dir)

    for item in item_list:
        filepath = os.path.join(target_dir, item)
        filename, file_extension = os.path.splitext(filepath)
        md5Str = getCheckSumOfFile(filepath,"md5")
        sha256Str = getCheckSumOfFile(filepath,"sha256")
        
        serialNumber = ""
        cuit=""
        if (item.endswith('.cer')):
            try:
                cuit = item.replace("cer_client-", "").replace(".cer", "")
                with open(filepath, 'rb') as f:
                    cert_data = f.read()
                x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
                serialNumber = hex(x509.get_serial_number())
            except FileNotFoundError as err:
                raise FileNotFoundError(f"File not found. {err}")
            except Exception as err:
                raise Exception(f"Fail to open file. {err}")

        if (item.endswith('.p12')):
            try:
                cuit = item.replace("p12_client-", "").replace(".p12", "")
                with open(filepath, 'rb') as f:
                    p12_data = f.read()

                bytes_password = cuit.encode('utf-8')
                private_key, cert, additional_certificates = pkcs12.load_key_and_certificates(
                    p12_data,
                    bytes_password
                )
                serialNumber = hex(cert.serial_number)
            except FileNotFoundError as err:
                raise FileNotFoundError(f"File not found. {err}")
            except Exception as err:
                raise Exception(f"Fail to open file. {err}")
            
        #main library that holds stats
        stats = os.stat(filepath)
        attrs = {
            'cuit':cuit,
            'file_name': item,
            'file_name_iskey': item.endswith('.key'),
            'file_extension': file_extension,
            'md5': md5Str,
            'sha256': sha256Str,
            'serialNumber':serialNumber,
            'size_kb': sizeFormat(stats.st_size),
            'creation_date': timeConvert(stats.st_ctime).__str__(),
            'modified_date': timeConvert(stats.st_mtime).__str__(),
            'last_access_date': timeConvert(stats.st_atime).__str__(),
        }

        if os.path.isdir(filepath):
            recursiveDict += get_files_recursive_metadata(filepath)
        else:
            recursiveDict[item] = attrs 

    return recursiveDict

def timeConvert(atime):
  dt = atime
  newtime = datetime.datetime.fromtimestamp(dt, tz=None)
  return newtime.date()
   
def sizeFormat(size):
    newform = format(size/1024, ".2f")
    return newform + " KB"

def csv_to_list(file_path) -> list:
    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter='\t') #, quotechar='"', quoting=csv.QUOTE_MINIMAL
            for row in csv_reader:
                line = csv_reader.line_num
                data_list.append(row)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(file_path, line, e))
    return data_list

def csv_to_dictionary(file_path)-> dict:
    data_dict=[]
    line=0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter='\t') #, quotechar='"', quoting=csv.QUOTE_MINIMAL
            data_dict = [row for row in csv_reader]
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(file_path, line, e))       
    return data_dict

def cleanFolderForFile(filepath):
    """
    Makes sure the folder exists for a given file and that the file doesn't exist.

    :param filepath: Path to the file we want to make sure the parent directory
                        exists.
    """
    if os.path.exists(filepath):
        os.remove(filepath)

def getCheckSumOfFile(filepath,algorithm):
    algo = None
    if algorithm == "sha256":
        algo = hashlib.sha256()
    elif algorithm == "sha512":
        algo = hashlib.sha512()
    elif algorithm == "md5":
        algo = hashlib.md5()
    else:
        sys.exit("Please specify a valid hashing algorithm (Either md5, sha256 or sha512)")

    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                algo.update(byte_block)
            digest = algo.hexdigest()
        return digest
    else:
        sys.exit("getCheckSumOfFile. File not found.")

    return None


def save_base64_to_pdf(base64_string, filename):
    """
    Saves base64 encoded data to a PDF file.
    Args:
        base64_string: The base64 encoded string.
        filename: The name of the PDF file to be saved.
    """
    try:
         # Decode the base64 string
        pdf_data = base64.b64decode(base64_string)
        # Check for PDF file signature
        if pdf_data[0:4] != b"%PDF":
            raise ValueError("Invalid PDF file or missing PDF file signature")
        # Write the decoded data to a PDF file
        with open(filename, "wb") as pdf_file:
            pdf_file.write(pdf_data)
        
        #print(f"PDF file saved successfully as {filename}")
    except Exception as err:
        raise Exception(f"save_base64_to_pdf. Fail to open file. {err}")

def file_to_base64(file_path):
    """
    Encodes a file to base64.
    Args:
        file_path (str): The path to the file.
    Returns:
        str: The base64 encoded string of the file content, or None if an error occurs.
    """
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
            
        return base64.b64encode(file_content).decode("utf-8")
    except FileNotFoundError:
        print(f"file_to_base64. Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"file_to_base64. An error occurred: {e}")
        return None
