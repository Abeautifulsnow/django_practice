import qrcode
from django.http import HttpResponse
from django.utils.six import BytesIO

# Create your views here.
def generate_qrcode(request, data):
    img = qrcode.make(data)

    buf = BytesIO()
    img.save(buf)
    image_steam = buf.getvalue()

    response = HttpResponse(image_steam, content_type="image/png")
    return response

