from io import BytesIO
import IPython
import json
import os
from PIL import Image
import requests
import time

STABILITY_KEY = '<your_key>'

def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response


def generate_image(prompt):
    aspect_ratio = "1:1"
    seed = 0
    output_format = "jpeg"

    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"
    params = {
        "prompt" : prompt,
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format" : output_format,
        "model" : "sd3-turbo"
    }

    response = send_generation_request(
        host,
        params
    )


    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")


    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")


    generated = f"generated_image.{output_format}"
    with open(generated, "wb") as f:
        f.write(output_image)

