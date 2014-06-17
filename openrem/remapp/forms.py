from django import forms

class SizeUploadForm(forms.Form):
    sizefile = forms.FileField(
        label='Select a file'
    )

class SizeHeadersForm(forms.Form):
    height_field = forms.CharField()
    weight_field = forms.CharField()
    id_field = forms.CharField()
    ID_TYPES = (("si-uid", "Study instance UID"), ("acc-no", "Accession Number"))
    id_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ID_TYPES)
    
