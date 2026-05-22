from django import forms
from accounts.models import User
from CodeStream.utils import role_selection


# ===========================================
# User Role Form (Access: Authenticated User)
# ===========================================
class UserRoleForm(forms.ModelForm):
  class Meta:
    model = User 
    fields = ["role"]
    
  def clean_role(self):
    role = self.cleaned_data.get("role").strip().lower()
    if not role:
      raise forms.ValidationError("please select a role.")
    if role not in role_selection:
      raise forms.ValidationError("Role must be (student or instructor)")
    return role


# ================================================
# Update Profile Form (Access: Authenticated User)
# ================================================
class UpdateProfileForm(forms.ModelForm):
  first_name = forms.CharField(max_length=20)
  last_name = forms.CharField(max_length=20)
  username = forms.CharField(max_length=10)

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

    if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
      raise forms.ValidationError("Username is already in use.")
    return username

  def clean_avatar(self):
    avatar = self.cleaned_data.get("avatar")
    return avatar



# ============================================================
# Update Profile Description Form (Access: Authenticated User)
# ============================================================
class UpdateProfileDescriptionForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["description"]

  def clean_description(self):
    description = self.cleaned_data.get("description", "").strip()
    return description