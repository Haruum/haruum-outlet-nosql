from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import order
import json


@require_POST
@api_view(['POST'])
def serve_register_order_to_outlet(request):
    """
    This view registers an order to the outlet specified
    by the laundry outlet email. The program first checks if the current
    workload is more than the quota. Then, if workload < quota, the view
    adds the workload of the laundry outlet.
    ---------------------------------------------
    request data must contain:
    laundry_outlet_email: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    order.register_order_to_outlet(request_data)
    response_data = {'message': 'Order is successfully registered'}
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
def serve_finish_order_from_outlet(request):
    """
    This view removes an order from the outlet specified
    by the laundry outlet email.
    ---------------------------------------------
    request data must contain:
    laundry_outlet_email: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    order.finish_order_from_outlet(request_data)
    response_data = {'message': 'Order is successfully removed'}
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
def serve_update_outlet_rating(request):
    """
    This view recomputes the outlet rating everytime an
    order review has been submitted.
    ---------------------------------------------
    request data must contain:
    laundry_outlet_email: string
    new_rating: integer
    """
    request_data = json.loads(request.body.decode('utf-8'))
    order.update_outlet_rating(request_data)
    response_data = {'message': 'Outlet rating is successfully recomputed'}
    return Response(data=response_data)

