from allauth.account.adapter import DefaultAccountAdapter

class CustomAdapter(DefaultAccountAdapter):
  def save_user(self, request, user, form, commit=False):
    user = super().save_user(request, user, form, commit=False)
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    
    if commit:
      user.save()
    return user