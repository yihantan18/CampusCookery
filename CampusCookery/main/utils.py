from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

def resize_profile_picture(image):
    PFP_SIZE = 256

    img = Image.open(image)

    # Crops image to a square
    width, height = img.size

    if width > height:
        left = (width - height) // 2
        top = 0
        right = width - left
        bottom = height
    else:
        left = 0
        top = (height - width) // 2
        right = width
        bottom = height - top

    img = img.crop((left, top, right, bottom))

    # Resize to 256x256
    img = img.resize((PFP_SIZE, PFP_SIZE), Image.Resampling.LANCZOS)

    # Return image as raw file for django
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return ContentFile(buffer.getvalue())
