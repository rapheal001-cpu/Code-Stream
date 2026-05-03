from django import forms
from .models import Course, CourseVideo

class CreateCourseForm(forms.ModelForm):
  class Meta:
    model = Course
    fields = ['name', 'thumbnail', 'description', 'price']
  
  def clean_name(self):
    name = self.cleaned_data.get('name', '').strip()
    return name

  def clean_description(self):
    description = self.cleaned_data.get('description', '').strip()
    return description

  def clean_price(self):
    price = self.cleaned_data.get('price')
    if price <= 0:
      raise forms.ValidationError('Enter a valid price for the course.')
    return price
  
  def clean_thumbnail(self):
    thumbnail = self.cleaned_data.get('thumbnail')
    if not thumbnail:
      raise forms.ValidationError('Thumbnail can not be empty.')
    return thumbnail


class UpdateCourseForm(forms.ModelForm):
  class Meta:
    model = Course
    fields = ['name', 'thumbnail', 'description']
  
  def clean_name(self):
    name = self.cleaned_data.get('name', '').strip()
    return name

  def clean_description(self):
    description = self.cleaned_data.get('description', '').strip()
    return description
  
  def clean_thumbnail(self):
    thumbnail = self.cleaned_data.get('thumbnail')
    if not thumbnail:
      raise forms.ValidationError('Thumbnail can not be empty.')
    return thumbnail


class CourseVideoForm(forms.ModelForm):
  class Meta:
    model = CourseVideo
    fields = ['title', 'description', 'video', 'thumbnail']
    
    def clean_title(self):
      title = self.cleaned_data.get('title').strip().title()
      if not title:
        raise forms.ValidationError('This field is required.')
      return title

    def clean_description(self):
      description = self.cleaned_data.get('description').strip()
      return description

    def clean_video(self):
      video = self.cleaned_data.get('video')
      if not video:
        raise forms.ValidationError('This field is required.')
      return video