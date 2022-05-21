# import modules
import os

import qrcode
from decouple import config
from django.conf import settings
from PIL import Image


# taking image which user wants
# in the QR code center
def generate_qr(user, logo, session_id):
    Logo_link = logo

    logo = Image.open(Logo_link)

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = basewidth / float(logo.size[0])
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    # taking url or text
    base_url = config("URL")
    url = f"{base_url}/api/verify/person/{session_id}/"

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = "#019ff2"

    # adding color to QR code
    QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert("RGB")

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    base_path = f"qr/{user}.png"
    path = os.path.join(settings.BASE_DIR, f"media/{base_path}")
    # save the QR code generated
    QRimg.save(path)

    print("QR code generated!")
    return base_path
