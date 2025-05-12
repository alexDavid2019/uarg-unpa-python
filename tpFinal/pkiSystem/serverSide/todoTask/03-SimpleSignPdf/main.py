#!pip install PyPDF2
#Successfully installed PyPDF2-3.0.1
#!pip install pyhanko
#Successfully installed certifi-2025.4.26 charset-normalizer-3.4.1 defusedxml-0.7.1 pyhanko-0.26.0 pyhanko-certvalidator-0.26.8 pyyaml-6.0.2 qrcode-8.1 requests-2.32.3 tzdata-2025.2 tzlocal-5.3.1 uritools-4.0.3 urllib3-2.4.0
#!pip install pyHanko[image-support]
#Successfully installed Pillow-11.2.1 python-barcode-0.15.1

import sys, os, base64, logging
from datetime import datetime
from tzlocal import get_localzone # pip install tzlocal

from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, timestamps, fields
from pyhanko.sign.fields import SigSeedSubFilter
from pyhanko_certvalidator import ValidationContext
from pyhanko import stamp

import PyPDF2 as pypdf

from pyhanko.sign.general import (
    load_cert_from_pemder,
    load_certs_from_pemder,
)


path_root = os.path.dirname(__file__)
filesRepo_dir = os.path.join(path_root, 'filesRepo')

def simpleMethodToSign():
    # Load signer key material from PKCS#12 file
    # This assumes that any relevant intermediate certs are also included
    # in the PKCS#12 file.
    pcks12File= os.path.join(filesRepo_dir, 'pkcs12File-1745156979.p12')

    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=pcks12File, passphrase=b'passphrase'
    )

    # Set up a timestamping client to fetch timestamps tokens
    #timestamper = timestamps.HTTPTimeStamper(
    #    url='http://tsa.example.com/timestampService'
    #)
    #https://gist.github.com/deeplook/130983de7220fdd64b35d0a76f53854d
    timestamp = datetime.now(tz=get_localzone())

    # Settings for PAdES-LTA
    signature_meta = signers.PdfSignatureMetadata(
        field_name='Signature', md_algorithm='sha256',
        # Mark the signature as a PAdES signature
        subfilter=SigSeedSubFilter.PADES,
        # We'll also need a validation context
        # to fetch & embed revocation info.
        validation_context=ValidationContext(allow_fetching=True),
        # Embed relevant OCSP responses / CRLs (PAdES-LT)
        embed_validation_info=True,
        # Tell pyHanko to put in an extra DocumentTimeStamp
        # to kick off the PAdES-LTA timestamp chain.
        use_pades_lta=True
    )

    pdfInputFile= os.path.join(filesRepo_dir, 'DNI_AEPD.pdf')
    pdfOuputFile= os.path.join(filesRepo_dir, 'DNI_AEPD_signed_1.pdf')
    #use https://signaturely.com/online-signature/ to create image png
    imgToInsert= os.path.join(filesRepo_dir, 'signature.png')

    #numeracion inversa en negativo. -1 ultima pagina, -2 ante ultima. 0 primera pagina.
    PAGE = -1
    # Specify the position and size of the stamp
    left = 100  # x coordinate of the lower left corner in points
    bottom = 100  # y coordinate of the lower left corner in points
    right = 200  # x coordinate of the upper right corner in points
    top = 200  # y coordinate of the upper right corner in points
    #box=(200, 600, 400, 660)
    with open(pdfInputFile, 'rb') as inf:
        w = IncrementalPdfFileWriter(inf)
        fields.append_signature_field(
            w, sig_field_spec=fields.SigFieldSpec(
                'Signature',PAGE, box=(left, bottom, right, top)
            )
        )

        pdf_signer = signers.PdfSigner(
            signature_meta, signer=signer, stamp_style=stamp.TextStampStyle(
                # the 'signer' and 'ts' parameters will be interpolated by pyHanko, if present
                stamp_text='Signed by: %(signer)s\nTime: %(ts)s',
                background=images.PdfImage(imgToInsert)
            ),
        )

        with open(pdfOuputFile, 'wb') as outf:
            pdf_signer.sign_pdf(w, output=outf)




def asyncMethodToSign():
    #The process generally involves the following steps:
    #- Prepare the PDF:
    #The PDF document is prepared for signing, which includes reserving space for the signature.
    #- Create a Hash:
    #A hash of the PDF content (excluding the signature placeholder) is generated.
    #- External Signing:
    #The hash is sent to an external system or device for signing.
    #- Apply the Signature:
    #The signature obtained from the external system is then applied to the reserved space in the PDF.

    # Load signer from CER file
    cerCAFile= os.path.join(filesRepo_dir, 'caAutoSigned-1745188534.crt')
    cerWithSignFile= os.path.join(filesRepo_dir, 'certificateFile-1745188535.cer')
    cert_obj = load_cert_from_pemder(cerWithSignFile)
    chain = list(load_certs_from_pemder(cerCAFile))

    pdfInputFile= os.path.join(filesRepo_dir, 'DNI_AEPD.pdf')
    pdfOuputFile= os.path.join(filesRepo_dir, 'DNI_AEPD_signed_1.pdf')


def main():
    simpleMethodToSign()
    #TODO asyncMethodToSign() crear metodo de firma en modo asincronico usando hash del pdf en lugar de todos los bytes del pdf en curso.

if __name__ == '__main__':
    main()

