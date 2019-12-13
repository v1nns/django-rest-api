from django.contrib.auth.models import User, Group
from rest_framework import serializers
from services.models import Checkout, Payment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkout
        fields = (
            'checkout_id', 
            'nfc', 
        )

class PaymentSerializer(serializers.ModelSerializer):
    checkout = CheckoutSerializer()
    
    class Meta:
        model = Payment
        fields = (
            'created', 
            'card_number',
            'checkout',
        )
