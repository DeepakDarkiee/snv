import base64
import json
import os


def encode_to_base64(image):
    with open(
        f"/home/deep/Live-Projects/snv_backend/snv/{image}", "rb"
    ) as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        encoded_image = f"data:image/jpeg;base64,{encoded_string}"
    return encoded_image
