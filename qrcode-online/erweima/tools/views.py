import qrcode
from django.http import HttpResponse
from django.utils.six import BytesIO
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'tools/index.html', {})


def generate_qrcode(request, data):
    img = qrcode.make(data)

    buf = BytesIO()
    img.save(buf)
    image_steam = buf.getvalue()

    response = HttpResponse(image_steam, content_type="image/png")
    return response
