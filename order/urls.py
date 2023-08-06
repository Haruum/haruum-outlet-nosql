from django.urls import path
from .views import (
    serve_register_order_to_outlet,
    serve_finish_order_from_outlet,
    serve_update_outlet_rating,
)


urlpatterns = [
    path('create/', serve_register_order_to_outlet),
    path('complete/', serve_finish_order_from_outlet),
    path('rating/', serve_update_outlet_rating),
]
