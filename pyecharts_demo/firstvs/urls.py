from django.urls import path
from firstvs import views

urlpatterns = [
    path('', views.index, name='index'),
]

app_name = 'firstvs'
