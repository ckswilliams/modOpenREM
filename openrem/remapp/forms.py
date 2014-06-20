from django import forms

class SizeUploadForm(forms.Form):
    sizefile = forms.FileField(
        label='Select a file'
    )

class SizeHeadersForm(forms.Form):
    height_field = forms.ChoiceField(choices='')

    def __init__(self, my_choice=None, **kwargs):
        super(SizeHeadersForm, self).__init__(**kwargs)
        if my_choice:

            self.fields['height_field'] = forms.ChoiceField(choices=my_choice)
            self.fields['weight_field'] = forms.ChoiceField(choices=my_choice)
            self.fields['id_field'] = forms.ChoiceField(choices=my_choice)
            ID_TYPES = (("si-uid", "Study instance UID"), ("acc-no", "Accession Number"))
            self.fields['id_type'] = forms.ChoiceField(widget=forms.RadioSelect, choices=ID_TYPES)

