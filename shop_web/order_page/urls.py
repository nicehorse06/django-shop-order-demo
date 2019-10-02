from django.urls import path
from . import views

app_name = 'order_page'
urlpatterns = [
    path('', views.hello, name='hello'),
]
