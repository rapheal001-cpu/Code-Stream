from django import forms
from accounts.models import User
from CodeStream.utils import role_selection


# User Role Form
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