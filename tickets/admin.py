from django.contrib import admin
from .models import Ticket, Cart, CartItem

# Register your models here.


admin.site.register(Ticket)
admin.site.register(Cart)
admin.site.register(CartItem)
