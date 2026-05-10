from django import forms
from .models import Course, CourseVideo


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "thumbnail", "description", "price"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip().title()
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Enter a valid price for the course.")
        return price

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")

        if not thumbnail:
            raise forms.ValidationError(
                "A thumbnail is required. Upload an image to represent your content."
            )

        if thumbnail.size > 2 * 1024 * 1024:
            raise forms.ValidationError(
                "Your image is too large. Please upload a file smaller than 2MB."
            )

        if not thumbnail.endwith((".jpg", ".jpeg", 'png')):
            raise forms.ValidationError(
                "Invalid file type. Please upload a valid image (JPG, PNG)."
            )

        return thumbnail


class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "thumbnail", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip().title()
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        return description

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")

        if not thumbnail:
            raise forms.ValidationError(
                "A thumbnail is required. Upload an image to represent your content."
            )

        if thumbnail.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Your image is too large. Please upload a file smaller than 2MB.')

        if not thumbnail.endwith((".jpg", ".jpeg", 'png')):
            raise forms.ValidationError('Invalid file type. Please upload a valid image (JPG, PNG).')

        return thumbnail


class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ["title", "description", "video", "thumbnail"]

        def clean_title(self):
            title = self.cleaned_data.get("title").strip().title()
            if not title:
                raise forms.ValidationError("This field is required.")
            return title

        def clean_description(self):
            description = self.cleaned_data.get("description").strip()
            return description

        def clean_video(self):
            video = self.cleaned_data.get("video")

            if not video:
                raise forms.ValidationError(
                    "A video is required. Please upload your content."
                )

            if video.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Your video is too large. Please upload a file smaller than 2MB.')

            if not video.endwith(".mp4"):
                raise forms.ValidationError('Invalid file type. Please upload a video (MP4).')

            return video


        def clean_thumbnail(self):
            thumbnail = self.cleaned_data.get("thumbnail")
            if not thumbnail:
                raise forms.ValidationError('A thumbnail is required. Upload an image to represent your content.')
            if thumbnail.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Your image is too large. Please upload a file smaller than 2MB.')
            if not thumbnail.endwith((".jpg", ".jpeg", 'png')):
                raise forms.ValidationError('Invalid file type. Please upload a file smaller than 2MB.')
