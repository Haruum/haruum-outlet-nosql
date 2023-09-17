from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from user_management.serializers.LaundryOutletSerializer import LaundryOutletSerializer
from .services import search


@require_GET
@api_view(['GET'])
def serve_get_outlets(request):
    """
    This view returns the list of all outlets.

    If a coordinate is provided, the view will order the result based
        on the distance of the outlet to the given coordinate.
    If an outlet name is provided, the view will only return outlets
        that matches the given name.
    ---------------------------------------------
    request data may contain:
    latitude: float
    longitude: float
    name: string
    """
    request_data = request.GET
    laundry_outlets = search.get_outlets(request_data)
    response_data = LaundryOutletSerializer(laundry_outlets, many=True).data
    return Response(response_data)


@require_GET
@api_view(['GET'])
def serve_get_outlet_provided_services(request):
    """
    This view returns the list of services provided by an outlet.
    ---------------------------------------------
    request data must contain:
    email: string
    """
    request_data = request.GET
    response_data = search.get_outlet_provided_services(request_data)
    return Response(data=response_data)

