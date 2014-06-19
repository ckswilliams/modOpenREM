from django import forms

class SizeUploadForm(forms.Form):
    sizefile = forms.FileField(
        label='Select a file'
    )

class SizeHeadersForm(forms.Form):
    
    LETTER_A = 'a'
    LETTER_B = 'b'
    CHOICES =  ((LETTER_A, 'letter a'),
                (LETTER_B, 'letter b'))
    
    choice = forms.ChoiceField(choices=CHOICES)
#    weight_field = forms.ChoiceField(choices=())
#    id_field = forms.ChoiceField(choices=())
#    ID_TYPES = (("si-uid", "Study instance UID"), ("acc-no", "Accession Number"))
#    id_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ID_TYPES)
    
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        choice = initial.get('choice', None)
        
        if choice:
            kwargs['initial']['choice'] = choice[0]
        
        super(forms.Form, self).__init__(*args, **kwargs)
        
        if choice and choice[0] not in (c[0] for c in self.CHOICES):
            print choice
            self.fields['choice'].choices.append(choice)
            print self.fields['choice'].choices
