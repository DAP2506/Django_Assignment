from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.db import models, CheckConstraint, Q, F


def validateMonth(value):
    if not (1 <= value <= 12):
        raise ValidationError(
            "Expiry month of credit/debit/prepaid cards must be in the range 1 <= month <= 12"
        )
    return value


def validate_number_length(value):
    if not 16 <= len(value) <= 19:
        raise ValidationError('Number length must be between 16 and 19 characters.')

class EBTCard(models.Model):
    number = models.CharField(
        max_length=19, 
        default="4111111111111111",
        validators=[validate_number_length]  # Added the custom validator
    )
    last_4 = models.CharField(max_length=4)
    
    # Constants for card brands that ACME supports
    TYPE_AMEX = "amex"
    TYPE_DISCOVER = "discover"
    TYPE_MASTERCARD = "mastercard"
    TYPE_VISA = "visa"
    CARD_BRAND_CHOICE = (
        (TYPE_AMEX, "Amex"),
        (TYPE_DISCOVER, "Discover"),
        (TYPE_MASTERCARD, "Mastercard"),
        (TYPE_VISA, "Visa"),
    )

    brand = models.CharField(max_length=255, choices=CARD_BRAND_CHOICE)
    
    # exp_month = models.PositiveSmallIntegerField(validators=[validateMonth])
    # exp_year = models.PositiveSmallIntegerField() # 2 digits, e.g. 26 instead of 2026


class CreditCard(models.Model):
    number = models.CharField(
        max_length=17, default="4111111111111111"
    )
    last_4 = models.CharField(max_length=4)
    
    # Constants for card brands that ACME supports
    TYPE_AMEX = "amex"
    TYPE_DISCOVER = "discover"
    TYPE_MASTERCARD = "mastercard"
    TYPE_VISA = "visa"
    CARD_BRAND_CHOICE = (
        (TYPE_AMEX, "Amex"),
        (TYPE_DISCOVER, "Discover"),
        (TYPE_MASTERCARD, "Mastercard"),
        (TYPE_VISA, "Visa"),
    )

    brand = models.CharField(max_length=255, choices=CARD_BRAND_CHOICE)
    exp_month = models.PositiveSmallIntegerField(validators=[validateMonth])
    exp_year = models.PositiveSmallIntegerField() # 2 digits, e.g. 26 instead of 2026


class Order(models.Model):
    # The total amount which needs to be paid by the customer, including taxes and fees
    order_total = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(0)],
    )

    # Constants for order statuses
    TYPE_DRAFT = "draft"
    TYPE_FAILED = "failed"
    TYPE_SUCCEEDED = "succeeded"
    ORDER_STATUS_CHOICE = (
        (TYPE_DRAFT, "draft"),
        (TYPE_FAILED, "failed"),
        (TYPE_SUCCEEDED, "succeeded"),
    )

    status = models.CharField(
        max_length=10, 
        choices=ORDER_STATUS_CHOICE, 
        default=TYPE_DRAFT
    )

    success_date = models.DateTimeField(
        "Date when an order was successfully charged",
        null=True,
        blank=True,
    )

    # UNCOMMENT THIS FIELD TO GET STARTED!
    #
    # The amount which can be paid for with EBT. It's not necessarily true that the
    # entire ebt_total will be satisfied with EBT tender.

    ebt_total = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)]
    )

    # adding database contraints for order_total >= ebt_total
    def save(self, *args, **kwargs):
        if(self.order_total >= self.ebt_total):
            super(Order, self).save(*args, **kwargs)
        else:
            raise Exception("ebt total cannot be greater than order total")


class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, db_index=True
    )

    # What the customer actually chose to pay on the payment_method
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(0)],
    )

    description = models.CharField(max_length=255)
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=1,
    )

    payment_method_id = models.PositiveIntegerField(default=1)
    payment_method = GenericForeignKey('content_type', 'payment_method_id')

    TYPE_CREDITCARD = "creditcard"
    TYPE_EBTCARD = "ebtcard"
    PAYMENT_METHOD_CHOICE = (
        (TYPE_CREDITCARD, "creditcard"),
        (TYPE_EBTCARD, "ebtcard"),
    )

    payment_card = models.CharField(
        max_length=10, 
        choices=PAYMENT_METHOD_CHOICE, 
        default=TYPE_CREDITCARD
    )
    

    # Constants for payment statuses
    TYPE_REQ_CONF = "requires_confirmation"
    TYPE_SUCCEEDED = "succeeded"
    TYPE_FAILED = "failed"
    PAYMENT_STATUS_CHOICE = (
        (TYPE_REQ_CONF, "requires_confirmation"),
        (TYPE_SUCCEEDED, "succeeded"),
        (TYPE_FAILED, "failed"),
    )

    status = models.CharField(
        max_length=24, 
        choices=PAYMENT_STATUS_CHOICE, 
        default=TYPE_REQ_CONF,
    )

    success_date = models.DateTimeField(
        "Date when a payment was successfully charged",
        null=True,
        blank=True,
    )

    last_processing_error = models.TextField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     content_type = None
        
    #     if self.payment_method:
    #         print("my payment method : ", self.payment_method)
    #         if self.payment_card == "creditcard":
    #             print("my payment card : ", self.payment_card)
    #             if isinstance(self.payment_method, CreditCard):
    #                 content_type = ContentType.objects.get_for_model(CreditCard)
    #         elif isinstance(self.payment_method, EBTCard):
    #             content_type = ContentType.objects.get_for_model(EBTCard)
        
    #     if content_type:
    #         self.content_type = content_type
    #         self.payment_method_id = self.payment_method

    #     super().save(*args, **kwargs)


    def save(self, *args, **kwargs):

        if self.payment_method:
            if isinstance(self.payment_method, CreditCard):
                self.content_type = ContentType.objects.get_for_model(CreditCard)
            elif isinstance(self.payment_method, EBTCard):
                self.content_type = ContentType.objects.get_for_model(EBTCard)
            self.payment_method_id = self.payment_method.id
        super().save(*args, **kwargs)




    
