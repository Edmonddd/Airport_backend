from django import forms

from ImageModule.models import Imagefile, Videofile

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Imagefile
        fields = ['type','image','description']

class ImageSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label='Name')
    date = forms.DateField(required=False, label='Date')
    type = forms.CharField(max_length=100, required=False, label='Type')

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Videofile
        fields = ['name', 'video','description']

class VideoSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    upload_date = forms.DateField(required=False)
