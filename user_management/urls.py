from django.urls import path
from .views import (
    serve_register_laundry_outlet,
    serve_check_email_password_match,
    serve_get_laundry_outlet_data,
    serve_update_laundry_outlet_data,
    serve_update_item_category_provided
)


urlpatterns = [
    path('register/', serve_register_laundry_outlet),
    path('check-password/', serve_check_email_password_match),
    path('data/', serve_get_laundry_outlet_data),
    path('update/', serve_update_laundry_outlet_data),
    path('services-provided/update/', serve_update_item_category_provided)
]
