from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
]
