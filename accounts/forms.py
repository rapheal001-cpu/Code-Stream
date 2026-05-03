from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import User


class CustomSignupForm(SignupForm):
  first_name = forms.CharField(max_length=20)
  last_name = forms.CharField(max_length=20)
  username = forms.CharField(max_length=10)
  email = forms.EmailField(max_length=255)
  
  def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name', '').strip().title()
    if not first_name:
      raise forms.ValidationError('First name is required.')
    return first_name

  def clean_last_name(self):
    last_name = self.cleaned_data.get('last_name', '').strip().title()
    if not last_name:
      raise forms.ValidationError('Last name is required.')
    return last_name

  def clean_username(self):
    username = self.cleaned_data.get('username', '').strip().lower()
    if not username:
      raise forms.ValidationError('Username is required.')
    if not username.isalnum():
      raise forms.ValidationError('Only alphanumeric characters are allowed.')
    if User.objects.filter(username__iexact=username).exists():
      raise forms.ValidationError('Username is already in use.')
    return username

  def clean_email(self):
    email = self.cleaned_data.get('email', '').strip().lower()
    if not email:
      raise forms.ValidationError('Email address is required.')
    if not email.endswith('@gmail.com'):
      raise forms.ValidationError('Please enter a valid email ending with @gmail.com')
    if User.objects.filter(email__iexact=email).exists():
      raise forms.ValidationError('Email address is already in use.')
    return email


class CustomLoginForm(LoginForm):
  def clean_login(self):
    login = self.cleaned_data.get('login', '').strip().lower()
    if not login:
      raise forms.ValidationError('Please provide your email or username to this field.')
    return login


class EditProfileForm(forms.ModelForm):
  first_name = forms.CharField(max_length=20, required=False)
  last_name = forms.CharField(max_length=20, required=False)
  username = forms.CharField(max_length=10, required=False)

  class Meta:
    model = User
    fields = ["first_name", "last_name", "username", "avatar"]

  def clean_first_name(self):
    first_name = self.cleaned_data.get("first_name", "").strip().title()
    if not first_name:
      raise forms.ValidationError("This field is required.")
    return first_name

  def clean_last_name(self):
    last_name = self.cleaned_data.get("last_name", "").strip().title()
    if not last_name:
      raise forms.ValidationError("This field is required.")
    return last_name

  def clean_username(self):
    username = self.cleaned_data.get("username", "").strip().lower()
    if not username:
      raise forms.ValidationError("This field is required.")
      
    qs = User.objects.filter(username=username).exclude(pk=self.instance.pk)
    if qs.exists():
      raise forms.ValidationError("This username is already in use.")
    return username

  def clean_avatar(self):
    avatar = self.cleaned_data.get("avatar")
    if avatar and avatar.size > 2 * 1024 * 1024:  # 2MB max
      raise forms.ValidationError("Avatar file is too large (max 2MB).")
    return avatar


class ProfileDescriptionForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["description"]