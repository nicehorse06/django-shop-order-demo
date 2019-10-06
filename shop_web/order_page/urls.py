from django.urls import path
from .views import OrderView, csv_export

app_name = 'order_page'
urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('csv_export/', csv_export, name='csv_export'),
]
