from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    price = models.PositiveIntegerField()
    CURRENCY_CHOICES = [
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound'),
            ('ETB', 'Ethiopian Birr'),
            ('JPY', 'Japanese Yen'),
            ('CNY', 'Chinese Yuan'),
            ('INR', 'Indian Rupee'),
            ('AED', 'UAE Dirham'),
            ('SAR', 'Saudi Riyal'),
            ('KES', 'Kenyan Shilling'),
            ('ZAR', 'South African Rand'),
            ]
    currency = models.CharField(max_length=30, choices=CURRENCY_CHOICES)

