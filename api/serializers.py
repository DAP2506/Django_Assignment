from rest_framework import serializers
from rest_framework import viewsets
from api.models import CreditCard, Payment, Order, EBTCard
from itertools import chain
from django.db.models import QuerySet
from django.contrib.contenttypes.models import ContentType


class EBTCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBTCard
        fields = [
            "id",
            "last_4",
            "brand",
            "number",
        ]

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = [
            "id",
            "last_4",
            "brand",
            "exp_month",
            "exp_year",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_total",
            "status",
            "success_date",
            "ebt_total",
        ]




class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.SerializerMethodField()
    def get_payment_method(self, obj):
        if isinstance(obj.payment_method, CreditCard):
            return CreditCardSerializer(obj.payment_method).data
        elif isinstance(obj.payment_method, EBTCard):
            return EBTCardSerializer(obj.payment_method).data
        raise serializers.ValidationError("Unexpected type of payment method")


    # print("PAYMENT SERIALIZER: ",payment_method) 
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "description",
            "payment_method", 
            "payment_method_id", 
            "content_type", 
            "status",
            "success_date",
            "last_processing_error",
        ]
    
    def create(self, validated_data):

        # print("validated_data: ", validated_data)

        order = validated_data.pop('order')
        amount = validated_data.pop('amount')
        description = validated_data.pop('description')
        status = validated_data.pop('status')
        payment_card = self.initial_data.get('payment_card')
        payment_method = self.initial_data.get('payment_method')

        # print("request_data: ", order, amount, description, status, payment_card, payment_method)  

        content_types = ContentType.objects.all()
        model = None
        model_index = 0
        for content_type in content_types:
            if content_type.model == payment_card:
                model = content_type.model_class()
                model_index = content_type.id
                break

        content_type = ContentType.objects.get_for_id(model_index)
        
        print("content_type: ", content_type)

        if  payment_card == "creditcard":
            payment_method = CreditCard.objects.get(pk=payment_method)
        elif payment_card == "ebtcard": 
            payment_method = EBTCard.objects.get(pk=payment_method)
        
        payment = Payment.objects.create(order=order, amount=amount, description=description, status=status, payment_method=payment_method, content_type=content_type, **validated_data)

        print("payment: ", payment)
        return payment


    
