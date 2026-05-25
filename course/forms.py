from cloudinary import CloudinaryResource
from cloudinary.forms import CloudinaryFileField
from django import forms
from django.core.validators import URLValidator
from prompt_toolkit.validation import ValidationError
from .models import Course, CourseVideo


class CourseForm(forms.ModelForm):
    thumbnail = CloudinaryFileField(options={"crop": True, "width": 200, "height": 200, "quality": 100})
    class Meta:
        model = Course
        fields = ["name", "thumbnail", "description", "price", "youtube_link", "github_link", "is_paid"]

    def clean_name(self):
        name = self.cleaned_data.get("name").strip().title()
        return name

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")
        if not thumbnail:
            raise forms.ValidationError("A thumbnail is required. Upload an image to represent your content.")
        if not thumbnail.name.endswith((".jpg", ".jpeg", ".png")):
            raise forms.ValidationError("Invalid file type. Please upload an image.")
        if thumbnail.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Your image is too large.')
        return thumbnail

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        return price

    def clean_youtube_link(self):
        youtube_link = self.cleaned_data.get("youtube_link")
        if youtube_link and "youtube.com" not in youtube_link:
            raise forms.ValidationError("Only YouTube links are allowed.")
        try:
            URLValidator(youtube_link)
        except ValidationError:
            raise forms.ValidationError("Enter a valid YouTube URL.")
        return youtube_link

    def clean_github_link(self):
        github_link = self.cleaned_data.get("github_link")
        if github_link:
            try:
                URLValidator(github_link)
            except ValidationError:
                raise forms.ValidationError("Enter a valid Github URL.")
            if "github.com" not in github_link:
                raise forms.ValidationError("Only Github links are allowed.")
        return github_link

    def clean_is_paid(self):
        is_paid = self.cleaned_data.get("is_paid")
        price = self.cleaned_data.get("price")

        if price and price > 0 and not is_paid:
            raise forms.ValidationError(
                "You set a price but marked the course as free. Enable 'Paid' or set the price to 0.")
        if is_paid and (not price or price <= 0):
            raise forms.ValidationError("You marked this as a paid course but didn't set a price.")
        return is_paid


class UpdateCourseForm(forms.ModelForm):
    thumbnail = CloudinaryFileField(options={"crop": True, "width": 200, "height": 200, "quality": 100})

    class Meta:
        model = Course
        fields = ["name", "thumbnail", "description", "youtube_link", "github_link"]

    def clean_name(self):
        name = self.cleaned_data.get("name").strip().title()
        return name

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")
        if not thumbnail or isinstance(thumbnail, CloudinaryResource):
            return thumbnail
        if not thumbnail.name.lower().endswith((".jpg", ".jpeg", ".png")):
            raise forms.ValidationError("Invalid file type. Please upload an image.")
        if thumbnail.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Your image is too large. Max 2MB.")
        return thumbnail

    def clean_description(self):
        description = self.cleaned_data.get("description").strip()
        return description

    def clean_youtube_link(self):
        youtube_link = self.cleaned_data.get("youtube_link")
        if youtube_link and "youtube.com" not in youtube_link:
            raise forms.ValidationError("Only YouTube links are allowed.")
        try:
            URLValidator(youtube_link)
        except ValidationError:
            raise forms.ValidationError("Enter a valid YouTube URL.")
        return youtube_link

    def clean_github_link(self):
        github_link = self.cleaned_data.get("github_link")
        if github_link:
            try:
                URLValidator(github_link)
            except ValidationError:
                raise forms.ValidationError("Enter a valid Github URL.")
            if "github.com" not in github_link:
                raise forms.ValidationError("Only Github links are allowed.")
        return github_link


class CourseVideoForm(forms.ModelForm):
    video = CloudinaryFileField(options={"crop": True, "width": 200, "height": 200, "quality": 100})
    class Meta:
        model = CourseVideo
        fields = ["name", "description", "video"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip().title()
        if not name:
            raise forms.ValidationError("A name is required.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        if not description:
            raise forms.ValidationError("A description is required.")
        return description

    def clean_video(self):
        video = self.cleaned_data.get("video")
        if not video:
            raise forms.ValidationError("A video is required.")
        if not video.name.lower().endswith((".mp4", ".avi", ".mov")):
            raise forms.ValidationError("Invalid file type. Please upload a video file.")
        if video.size > 200 * 1024 * 1024:
            raise forms.ValidationError("Your video is too large. Max 200MB.")
        return video


class UpdateCourseVideoForm(forms.ModelForm):
    thumbnail = CloudinaryFileField(options={"crop": True, "width": 200, "height": 200})
    class Meta:
        model = CourseVideo
        fields = ["name", "description", 'thumbnail']

    def clean_name(self):
        name = self.cleaned_data.get("name").strip().title()
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description").strip()
        return description

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")
        if not thumbnail or isinstance(thumbnail, CloudinaryResource):
            return thumbnail
        if not thumbnail.name.lower().endswith((".jpg", ".jpeg", ".png")):
            raise forms.ValidationError("Invalid file type. Please upload an image.")
        if thumbnail.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Your image is too large. Max 2MB.")
        return thumbnail