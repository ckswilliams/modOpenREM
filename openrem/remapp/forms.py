from django import forms

class SizeUploadForm(forms.Form):
    sizefile = forms.FileField(
        label='Select a file'
    )
