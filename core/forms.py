from django import forms
from accounts.models import User

# User Role Form
class UserRoleForm(forms.ModelForm):
  class Meta:
    model = User 
    fields = ["role"]
    
  def clean_role(self):
    role = self.cleaned_data.get("role", "").strip().lower()
    if not role:
      raise forms.ValidationError("please select a role.")
    if role not in ['student', 'instructor']:
      raise forms.ValidationError("Role must be (student or instructor)")
    return role