from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import User


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=255)

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip().title()
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip().title()
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip().lower()
        if not username.isalnum():
            raise forms.ValidationError("Only alphanumeric characters are allowed.")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("Username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError(
                "Please enter a valid email ending with @gmail.com"
            )
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Email address is already in use.")
        return email


class CustomLoginForm(LoginForm):
    def clean_login(self):
        login = self.cleaned_data.get("login", "").strip().lower()
        return login


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    username = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "avatar"]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip().title()
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip().title()
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip().lower()
        if not username.isalnum():
            raise forms.ValidationError("Only alphanumeric characters are allowed.")
        qs = User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Username is already in use.")
        return username

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image must be less than 2MB.")
        return avatar


class ProfileDescriptionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["description"]

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        return description
