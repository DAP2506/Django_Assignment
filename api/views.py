# See the fixtures/ directory for examples of the request bodies
# needed to create objects using the ListCreateAPIViews below.

from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Payment, CreditCard, Order, EBTCard
from api.serializers import PaymentSerializer, CreditCardSerializer, OrderSerializer, EBTCardSerializer
from processor import processPayment
from django.contrib.contenttypes.models import ContentType

import json

# done
class ListCreateEBTCard(APIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/ebt_cards/ <- returns a list of all EBTCard objects
    2. POST http://localhost:8000/api/ebt_cards/ <- creates a single EBTCard object and returns it

    """
    # This is the way to call GET request in django 

    def get(self, request, format=None):
        queryset = EBTCard.objects.all()
        serializer = EBTCardSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # This is the way to call POST request in django 

    def post(self, request, format=None):
        serializer = EBTCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# done
class RetrieveDeleteEBTCard(APIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/ebt_cards/:id/ <- returns a EBTCard object provided its id.
    2. DELETE http://localhost:8000/api/ebt_cards/:id/ <- deletes a EBTCard object by id.

    """

    def get(self, request, *args, **kwargs):
        card_id = self.kwargs['id']  # Access the ID passed in the URL
        try:
            queryset = EBTCard.objects.get(id=card_id)  # Retrieve the card by ID
            serializer = EBTCardSerializer(queryset)  # Use serializer for a single object
            return Response(serializer.data)
        except EBTCard.DoesNotExist:
            return Response({"detail": "EBTCard not found."}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, *args, **kwargs):
        card_id = self.kwargs['id']  
        try:
            ebt_card = EBTCard.objects.get(id=card_id)
            ebt_card.delete()
            return Response({"detail": "EBTCard deleted."}, status=status.HTTP_204_NO_CONTENT)
        except EBTCard.DoesNotExist:
            return Response({"detail": "EBTCard not found."}, status=status.HTTP_404_NOT_FOUND)



# done
class ListCreateCreditCard(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/credit_cards/ <- returns a list of all CreditCard objects
    2. POST http://localhost:8000/api/credit_cards/ <- creates a single CreditCard object and returns it

    """
    # This is the way to call GET request in django 

    def get(self, request, *args, **kwargs):
        queryset = CreditCard.objects.all()
        serializer_class = CreditCardSerializer
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    # This is the way to call POST request in django 

    def post(self, request, format=None):
        serializer = CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# done
class RetrieveDeleteCreditCard(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/credit_cards/:id/ <- returns a CreditCard object provided its id.
    2. DELETE http://localhost:8000/api/credit_cards/:id/ <- deletes a CreditCard object by id.

    """
    def get(self, request, *args, **kwargs):
        card_id = self.kwargs['pk']  # Access the ID passed in the URL
        try:
            queryset = CreditCard.objects.get(id=card_id)  # Retrieve the card by ID
            serializer = CreditCardSerializer(queryset)  # Use serializer for a single object
            return Response(serializer.data)
        except CreditCard.DoesNotExist:
            return Response({"detail": "CreditCard not found."}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, *args, **kwargs):
        card_id = self.kwargs['pk']  
        try:
            credit_card = CreditCard.objects.get(id=card_id)
            credit_card.delete()
            return Response({"detail": "C4reditCard deleted."}, status=status.HTTP_204_NO_CONTENT)
        except CreditCard.DoesNotExist:
            return Response({"detail": "CreditCard not found."}, status=status.HTTP_404_NOT_FOUND)


# done
class ListCreateOrder(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/orders/ <- returns a list of all Order objects
    2. POST http://localhost:8000/api/orders/ <- creates a single Order object and returns it

    """
    
    # This is the way to call GET request in django 

    def get(self, request, *args, **kwargs):
        print("GET request from /api/orders/ ")
        queryset = Order.objects.all()
        serializer_class = OrderSerializer
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    # This is the way to call POST request in django 

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# done
class RetrieveDeleteOrder(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/orders/:id/ <- returns an Order object provided its id.
    2. DELETE http://localhost:8000/api/orders/:id/ <- deletes an Order object by id.

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['id']  # Access the ID passed in the URL
        try:
            queryset = Order.objects.get(id=order_id)  # Retrieve the card by ID
            serializer = OrderSerializer(queryset)  # Use serializer for a single object
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, *args, **kwargs):
        order_id = self.kwargs['id']  
        try:
            oorder = Order.objects.get(id=order_id)
            oorder.delete()
            return Response({"detail": "Order deleted."}, status=status.HTTP_204_NO_CONTENT)
        except EBTCard.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)




# done
class ListCreatePayment(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/payments/ <- returns a list of all Payment objects
    2. POST http://localhost:8000/api/payments/ <- creates a single Payment object and associates it with the Order in the request body.

    """
    # queryset = Payment.objects.all()
    # serializer_class = PaymentSerializer
    

    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(pk=order_id)
        payment = Payment.objects.create(order=order, **validated_data)
        return payment


    def get(self, request, *args, **kwargs):
        queryset = Payment.objects.all()
        serializer_class = PaymentSerializer
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    


    def post(self, request, *args, **kwargs):

        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment = serializer.save()
            return Response({'message': 'Payment created successfully', 'payment_id': payment.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    


# not done
class RetrieveDeletePayment(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/payments/:id/ <- returns a Payment object provided its id.
    2. DELETE http://localhost:8000/api/payments/:id/ <- deletes a Payment object by id.

    """
    # queryset = Payment.objects.all()
    # serializer_class = PaymentSerializer
    print('HI')
    def get(self, request, *args, **kwargs):
        payment_id = self.kwargs['id']
        try:
            queryset = Payment.objects.get(id=payment_id)
            serializer = PaymentSerializer(queryset)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        
        payment_id = self.kwargs['id']  
        try:
            ppayment = Order.objects.get(id=payment_id)
            ppayment.delete()
            return Response({"detail": "payment deleted."}, status=status.HTTP_204_NO_CONTENT)
        except EBTCard.DoesNotExist:
            return Response({"detail": "payment not found."}, status=status.HTTP_404_NOT_FOUND)
    


# done
class CaptureOrder(APIView):
    """ Provided an Order's id, submit all associated payments to the payment processor.

    Payments will change status to either failed or succeeded, depending on the
    response from the payment processor.

    Once all payments have been processed, the status of the Order object will be updated
    to 'suceeded' if all of the payments were successful or 'failed' if at least one payment
    was not successful.
    """

    def post(self, request, id):
        try:
            order_obj = Order.objects.get(id=id) # throws if order_id not found

            # Find all Payments associated with this Order via /api/payments/
            payment_queryset = Payment.objects.filter(order__id=id)

        
            # print("PAYMENT QUERYSET: ",payment_queryset) 
            # for payments in payment_queryset:
            #     if payments.payment_card == 'ebtcard':
            #         print("EBT PAYMENTS: ",payments.amount)
            #     else:
            #         print("CREDIT PAYMENTS: ",payments.amount)

            # Payments must satisfy the order_total
            total_payment_amount = sum([x.amount for x in payment_queryset])
            if total_payment_amount != order_obj.order_total:
                print("Total payment amount: ", total_payment_amount)
                print("Order total: ", order_obj.order_total)
                return Response({
                    "error_message": "Payment total does not match order total for Order with id {}".format(id)
                }, status=status.HTTP_400_BAD_REQUEST)

            
            # Payments must satisfy the EBT total

            
            ebt_payments_amount = sum([payment.amount for payment in payment_queryset if payment.content_type.model == 'ebtcard'])
            print("EBT PAYMENTS AMOUNT: ",ebt_payments_amount)
            if ebt_payments_amount > order_obj.ebt_total:
                return Response({"error_message": "Total amount of payments with EBT cards exceeds EBT eligibility for Order with id {}".format(id)}, status=status.HTTP_400_BAD_REQUEST)


            potential_errors = []
            for payment in payment_queryset:
                potential_error = processPayment(payment)

                if potential_error:
                    potential_errors.append(potential_error)

            if potential_errors:
                order_obj.status = Order.TYPE_FAILED
            else:
                order_obj.status = Order.TYPE_SUCCEEDED
                order_obj.success_date = timezone.now()

            order_obj.save() # write status back to database

            return Response(
                OrderSerializer(order_obj).data
            )

        except Order.DoesNotExist:
            return Response({
                "error_message": "Unable to find Order with id {}".format(id)
            }, status=status.HTTP_404_NOT_FOUND)
