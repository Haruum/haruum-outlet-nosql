from django.db import transaction
from django.views.decorators.http import require_POST, require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import LaundryOutletSerializer
from .services import auth
import json


@require_POST
@api_view(['POST'])
def serve_register_laundry_outlet(request):
    """
    This view registers a laundry outlet based
    on the data given in the request body.
    ---------------------------------------------
    request data must contain:
    email: string,
    phone_number: string,
    name: string
    address: string
    password: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    laundry_outlet = auth.register_laundry_outlet(request_data)
    response_data = LaundryOutletSerializer(laundry_outlet).data
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
def serve_check_email_password_match(request):
    """
    This view validates the correctness of the password
    with respect of the email given in the request data.
    ---------------------------------------------
    request data must contain:
    email: string
    password: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    password_is_for_email = auth.check_email_and_password(request_data)
    response_data = {'password_is_for_email': password_is_for_email}
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_laundry_outlet_data(request):
    """
    This view returns Outlet's name, address, phone number,
    email, Quota, and Availability Status
    ---------------------------------------------
    request data must contain:
    email: string
    """
    request_data = request.GET
    laundry_outlet = auth.get_laundry_outlet_data(request_data)
    response_data = LaundryOutletSerializer(laundry_outlet).data
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
@transaction.atomic()
def serve_update_laundry_outlet_data(request):
    """
    This view updates the laundry outlet data
    (availability status, quota, address)
    ---------------------------------------------
    request data must contain:
    email: string
    is_available: bool
    quota: integer
    address: string
    phone_number: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    auth.update_outlet_data(request_data)
    response_data = {'message': 'Outlet is updated successfully'}
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
@transaction.atomic()
def serve_update_item_category_provided(request):
    """
    This view updates the laundry outlet provided services.
    ---------------------------------------------
    request data must contain:
    email: string
    services_provided: list

    services_provided follows the following format
    {
        service_category_id: uuid string
        price_per_item: float
    }
    """
    request_data = json.loads(request.body.decode('utf-8'))
    auth.update_item_category_provided(request_data)
    response_data = {'message': 'Service item category is successfully updated'}
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_check_outlet_existence(request):
    """
    This view checks whether an outlet corresponding to the
    given email exists in the database.
    ---------------------------------------------
    request param must contain:
    email: string
    """
    request_data = request.GET
    outlet_exists = auth.check_outlet_existence(request_data)
    response_data = {'outlet_exists': outlet_exists}
    return Response(data=response_data)

