from django.contrib import admin
from .models import (User, Notification, Wallet, PaymentHistory, OrderHistory, )

# Register your models here.
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Wallet)
admin.site.register(PaymentHistory)
admin.site.register(OrderHistory)
