from rest_framework import serializers
from rest_framework import viewsets

from api.models import CreditCard, Payment, Order, EBTCard


class PaymentMethodField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return CreditCard.objects.all() | EBTCard.objects.all()

    def to_representation(self, value):
        if isinstance(value, CreditCard):
            return CreditCardSerializer(value).data
        elif isinstance(value, EBTCard):
            return EBTCardSerializer(value).data
        else:
            raise Exception('Unexpected type of tagged object')



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
            # "ebt_total",
        ]

class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "description",
            "payment_method",
            "status",
            "success_date",
            "last_processing_error"
        ]




class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()  # Or whatever queryset you need
    serializer_class = PaymentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['payment_method_queryset'] = CreditCard.objects.all() | EBTCard.objects.all()
        return context

# class PaymentSerializer(serializers.ModelSerializer):
#     payment_method = PaymentMethodField(queryset=CreditCard.objects.all() | EBTCard.objects.all(), allow_null=True)

#     class Meta:
#         model = Payment
#         fields = [
#             "id",
#             "order", # The id of the associated Order object
#             "amount",
#             "description",
#             "payment_method", # The id of the associated CreditCard object or edbtcard object
#             "status",
#             "success_date",
#             "last_processing_error"
#         ]
