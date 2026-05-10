from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.urls import reverse
from CodeStream.utils import USER_ROLE, PAYMENT_TYPE, STATUS_TYPE
# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to="accounts/avatar/upload", blank=True, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLE)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following")
    profile_views = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="viewed_by")
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def unread_notification(self):
        return self.user_notification.filter(is_read=False).count()

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def wallet_balance(self):
        return self.wallet.balance

    @property
    def payment_history_list(self):
        return self.user_payment_history

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notification")
    title = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.user}, Message: {self.message[:20]}"

    def get_absolute_url(self):
        return reverse("notification-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("wallet", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user} - ${self.balance}"


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_payment_history")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE)
    status = models.CharField(max_length=10, choices=STATUS_TYPE)
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> ({self.payment_type})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment History"
        verbose_name_plural = "Payment Histories"

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order_payment_history")
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> ({self.title}) --> ({self.status})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order History"
        verbose_name_plural = "Order Histories"