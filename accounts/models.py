from cloudinary.models import CloudinaryField
from django.core.validators import validate_email, FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.urls import reverse
from CodeStream.utils import USER_ROLE, PAYMENT_TYPE, STATUS_TYPE
# Create your models here.


class User(AbstractUser):
    avatar = CloudinaryField(resource_type='image', folder='accounts/avatars/', null=True, blank=True, verbose_name="Avatar")
    first_name = models.CharField(max_length=20, verbose_name="First Name")
    last_name = models.CharField(max_length=20, verbose_name="Last Name")
    username = models.CharField(max_length=10, unique=True, verbose_name="Username")
    email = models.EmailField(validators=[validate_email], max_length=255, unique=True, verbose_name="Email Address")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    role = models.CharField(max_length=10, choices=USER_ROLE, verbose_name="Role")
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following", verbose_name="Followers")
    views = models.ManyToManyField("self", symmetrical=False, blank=True, verbose_name="Views")

    def __str__(self):
        return f"{self.username} ({self.role})"

    def get_absolute_url(self):
        return reverse("profile-view", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def unread_notification(self):
        return self.notifications.filter(is_read=False).count()

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def wallet_balance(self):
        return self.wallet.balance

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", verbose_name="User")
    name = models.CharField(max_length=255, verbose_name="Name")
    sender = models.CharField(max_length=30, default="System Notification", verbose_name="Sender")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Read")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender}, To: {self.user}, Message: {self.message[:20]}"

    def get_absolute_url(self):
        return reverse("notification-detail-view", kwargs={"pk": self.pk})

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
        return reverse("wallet-view", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user}  (${self.balance})"


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_history", verbose_name="User")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, verbose_name="Payment Type")
    status = models.CharField(max_length=10, choices=STATUS_TYPE, verbose_name="Payment Status")
    message = models.CharField(max_length=300, verbose_name="Payment Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.user} ({self.payment_type} - {self.status})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment History"
        verbose_name_plural = "Payment Histories"


class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_payment_history", verbose_name="User")
    name = models.CharField(max_length=255, verbose_name="Name")
    message = models.CharField(max_length=300, verbose_name="Message")
    status = models.CharField(max_length=10, choices=STATUS_TYPE, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.user} --> ({self.name} - {self.status})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order History"
        verbose_name_plural = "Order Histories"