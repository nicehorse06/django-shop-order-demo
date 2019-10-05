from django.urls import path
from .views import OrderView, some_view

app_name = 'order_page'
urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('test/', some_view, name='test'),
]
