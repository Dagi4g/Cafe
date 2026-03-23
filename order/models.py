from django.db import models


class Cafe(models.Model):
    name = models.CharField(max_length=255)
    # logo = models.ImageField(upload_to='cafe_logos/')

    def __str__(self):
        return self.name


class Table(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='tables')
    table_id = models.CharField(max_length=50)

    def __str__(self):
        return f"Chair {self.table_id} ({self.cafe.name})"


class Chair(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='chairs')
    chair_id = models.CharField(max_length=50)

    def __str__(self):
        return f"Table {self.chair_id}"


class Menu(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return self.name


class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='orders')
    cart = models.PositiveIntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order {self.id} - {self.item.name}"
