from django.urls import path
from .views import OrderView

app_name = 'order_page'
urlpatterns = [
    path('', OrderView.as_view(), name='order'),
]
