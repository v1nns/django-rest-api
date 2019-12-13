from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from services.serializers import UserSerializer, GroupSerializer

# new
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# mine
from services.models import Checkout, Payment
from services.serializers import CheckoutSerializer, PaymentSerializer
import logging

# self services
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CheckoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    
class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
# Get an instance of a logger
logger = logging.getLogger(__name__)
    
# Mobile services
@api_view(['POST'])
def requestPayment(request):
    """
    Save a new payment instance.
    """
    try:
        pos = Checkout.objects.get(nfc=request.data['checkout']['nfc'])
    except Checkout.MultipleObjectsReturned:
        logger.error('1 - Something went wrong!')
        return Response('multiple checkouts', status=status.HTTP_400_BAD_REQUEST)
    except Checkout.DoesNotExist:
        logger.error('2 - Something went wrong!')
        return Response('does not exist', status=status.HTTP_400_BAD_REQUEST)
    
    logger.error('3 - Something went wrong!')
    
    # check its length
    card_number = request.data['card_number']
    if len(card_number) != 16:
        return Response('size of card must be 16 characters',status=status.HTTP_400_BAD_REQUEST)
    
    #checkout_serializer = CheckoutSerializer(pos)
    payment_request = Payment.objects.create(card_number = card_number, checkout = pos)    
    payment_serializer = PaymentSerializer(payment_request)
    
    logger.error('4 - Something went wrong!')
    
    return Response(payment_serializer.data)
    
# @api_view(['GET'])
# def getPaymentStatus(request, card_number):
    # """
    # Get status from an existent payment instance.
    # """
    # queryset = Payment.objects.all()
    # if queryset:
        # serializer = PaymentSerializer(queryset, many=True)
        # return Response(serializer.data)
    # else:
        # return Response(status=status.HTTP_404_NOT_FOUND)    

# POS services
@api_view(['GET'])
def getPaymentRequests(request):
    """
    Get any existent payment request instance.
    """
    queryset = Payment.objects.all()
    if queryset:
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
@api_view(['GET'])
def getPaymentRequest(request, checkout):
    """
    Get the first payment request instance.
    """
    query = Payment.objects.filter(checkout__checkout_id = checkout).first()
    
    if query:
        serializer = PaymentSerializer(query)
        # TODO - delete the query from stack
        # query.delete()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def removeCheckouts(request):
    """
    Delete any existent card instance.
    """
    try:
        Checkout.objects.all().delete()
    except Payment.DoesNotExist:
        return Response('There are no payment requests to remove', status=status.HTTP_404_NOT_FOUND)

    return Response('Removed all payment requests with success', status=status.HTTP_200_OK)
    
@api_view(['DELETE'])
def removePaymentRequests(request):
    """
    Delete any existent card instance.
    """
    try:
        Payment.objects.all().delete()
    except Payment.DoesNotExist:
        return Response('There are no payment requests to remove', status=status.HTTP_404_NOT_FOUND)

    return Response('Removed all payment requests with success', status=status.HTTP_200_OK)