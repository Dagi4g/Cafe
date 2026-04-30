from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import UniqueConstraint



class Cafe(models.Model):
    name = models.CharField(max_length=255,unique=True)
    # logo = models.ImageField(upload_to='cafe_logos/')

    def __str__(self):
        return self.name


class Table(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='tables')
    table_id = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.table_id} ({self.cafe.name})"
    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['cafe','table_id'], name='unique_cafe_table')
                                        ]



class Chair(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='chairs')
    chair_id = models.PositiveIntegerField()
    occupied = models.BooleanField(default=False)
                                           
    occupied_at = models.DateTimeField(null=True, blank=True)  # When it became occupied


    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['table','chair_id'], name='unique_table_chair')
                                        ]


    def occupy(self):
        """Mark chair as occupied with timestamp"""
        self.occupied = True
        self.occupied_at = timezone.now()
        self.save()
    
    def release(self):
        """Manually release chair"""
        self.occupied = False
        self.occupied_at = None
        self.save()
    
    @property
    def is_occupied(self):
        """Check if chair is still occupied (accounting for timeout)"""
        if not self.occupied:
            return False
        
        # Check if timeout has passed
        if self.occupied_at:
            timeout = timezone.now() - self.occupied_at
            if timeout > timedelta(minutes=1):
                # Auto-release if expired
                self.release()
                return False
        
        return self.occupied
    
    def save(self, *args, **kwargs):
        """Auto-check expiration on save"""
        if self.occupied and self.occupied_at:
            if timezone.now() - self.occupied_at > timedelta(hours=1):
                self.occupied = False
                self.occupied_at = None
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Chair {self.chair_id}"

   


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
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        PREPARING = 'preparing', 'Preparing'
        READY = 'ready', 'Ready'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'
        

    order_time = models.DateTimeField(auto_now_add=True)
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    @property
    def is_expired(self):
        timeout = timezone.now() - self.order_time
        if self.status == self.Status.PENDING and timeout > timedelta(minutes=30):
            self.delete()
            return True
        return False



    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def total_price(self):
        return self.price * self.quantity

    
    def __str__(self):
        return f"{self.food.name} x {self.quantity}"
