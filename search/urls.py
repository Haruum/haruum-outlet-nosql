from django.urls import path
from .views import (
    serve_get_outlets,
    serve_get_outlet_provided_services,
)


urlpatterns = [
    path('outlets/', serve_get_outlets),
    path('outlet/services/', serve_get_outlet_provided_services),
]
