from django.db import models

# Create your models here.

class Checkout(models.Model):
    # Fields
    checkout_id = models.IntegerField(max_length=3)
    nfc = models.CharField(max_length=17)
    
    class Meta:
        app_label = 'restserver'
        ordering = ('checkout_id',)

    
class Payment(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    card_number = models.CharField(max_length=16)

    # Relationship Fields
    checkout = models.ForeignKey('Checkout', on_delete=models.PROTECT)

    class Meta:
        app_label = 'restserver'
        ordering = ('created',)