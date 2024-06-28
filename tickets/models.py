from django.db import models
from django.contrib.auth.models import User
import string, random, uuid

# Create your models here.


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default='tickets/images/ticket_image.jpg')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='pending')
    unique_id = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:10])

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.ticket.name}"


def generate_unique_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_key = models.CharField(max_length=10, unique=True, default=generate_unique_key)

    def __str__(self):
        return self.user.username


class AdminLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Creation'),
        ('delete', 'Suppression')
    ]

    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=6, choices=ACTION_CHOICES)
    ticket_name = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} {self.action} {self.ticket_name}"