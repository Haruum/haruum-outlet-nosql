from django.urls import path
from .views import (
    serve_get_outlets,
    serve_get_outlet_provided_services,
    serve_get_predetermined_service_categories
)


urlpatterns = [
    path('outlets/', serve_get_outlets),
    path('outlet/services/', serve_get_outlet_provided_services),
    path('predetermined-services/', serve_get_predetermined_service_categories)
]
