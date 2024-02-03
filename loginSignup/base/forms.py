from django import forms

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Your Label')

class FileUploadForm(forms.Form):
    file = forms.FileField()

