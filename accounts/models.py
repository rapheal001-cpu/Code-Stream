from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class User(AbstractUser):
  USER_ROLE = [
    ("", "--Select Role--"),
    ("student", "Student"),
    ("instructor", "Instructor")
    ]

  avatar = models.ImageField(upload_to='accounts/avatar/upload', default='accounts/avatar/default/avatar.png')
  description = models.TextField(null=True, blank=True)
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  username = models.CharField(max_length=10, unique=True)
  email = models.EmailField(max_length=255, unique=True)
  role = models.CharField(max_length=15, choices=USER_ROLE)
  followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following")
  profile_views = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="viewed_by")
  slug = models.SlugField(unique=True)
  
  def __str__(self):
    return f'{self.username} ({self.role})'
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.username)
    super().save(*args, **kwargs)
  
  def get_absolute_url(self):
    return reverse("profile", kwargs={"slug": self.slug})
    
  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'
  
  @property
  def unread_notification(self):
    return self.user_notification.objects.filter(is_read=False).count()

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
  def instructor_activated(self):
    return self.instructoractivation.activated
  
  class Meta:
    ordering = ['-date_joined']
    verbose_name = 'User'
    verbose_name_plural = 'Users'


class Notification(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notification")
  title = models.CharField(max_length=255)
  message = models.TextField()
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'To: {self.user.username}, Message: {self.message[:20]}'
    
  def get_absolute_url(self):
    return reverse("notification-detail", kwargs={"pk": self.pk})
  
  class Meta:
    ordering = ['-created_at']
    verbose_name = 'Notification'
    verbose_name_plural = 'Notifications'


class Wallet(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal("0.00"))
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
    
  def get_absolute_url(self):
    return reverse("wallet", kwargs={"pk":self.pk})

  class Meta:
    ordering = ["-created_at"]
    verbose_name = "Wallet"
    verbose_name_plural = "Wallets"

  def __str__(self):
    return f"{self.user.username} - ${self.balance} - ({self.user.role})"


class InstructorActivation(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  activated = models.BooleanField(default=False)
  amount = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.00'))
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'{self.user.username} -> {self.user.role} --> {self.activated}'
    
  class Meta:
    ordering = ['-created_at']
    verbose_name = "Instructor Activation"
    verbose_name_plural = "Instructor Activations"