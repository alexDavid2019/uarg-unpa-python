#!pip install PyPDF2
#Successfully installed PyPDF2-3.0.1
#!pip install pyhanko
#Successfully installed certifi-2025.4.26 charset-normalizer-3.4.1 defusedxml-0.7.1 pyhanko-0.26.0 pyhanko-certvalidator-0.26.8 pyyaml-6.0.2 qrcode-8.1 requests-2.32.3 tzdata-2025.2 tzlocal-5.3.1 uritools-4.0.3 urllib3-2.4.0
#!pip install pyHanko[image-support]
#Successfully installed Pillow-11.2.1 python-barcode-0.15.1


import sys, os, base64, logging
from datetime import datetime
from tzlocal import get_localzone # pip install tzlocal

import PyPDF2 as pypdf


path_root = os.path.dirname(__file__)
filesRepo_dir = os.path.join(path_root, 'filesRepo')

def simpleMethodToProtectPdf():
   
    pdfInputFile= os.path.join(filesRepo_dir, 'DNI_AEPD.pdf')
    pdfOuputFile= os.path.join(filesRepo_dir, 'DNI_AEPD_password_12345678.pdf')

    # Create reader and writer object
    reader = pypdf.PdfReader(pdfInputFile)
    writer = pypdf.PdfWriter()
    # Add all pages to writer (accepted answer results into blank pages)
    for page in reader.pages:
        writer.add_page(page)
    # Encrypt with your password: 12345678
    writer.encrypt('12345678')
    # Write it to an output file
    with open(pdfOuputFile, 'wb') as resultPdf:
        writer.write(resultPdf)

def main():
    simpleMethodToProtectPdf()

if __name__ == '__main__':
    main()

