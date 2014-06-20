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



#    height_field = forms.ChoiceField(choices=())



#    def __init__(self, *args, **kwargs):
#        initial = kwargs.get('initial', {})
#        choicepassed = initial.get('choice', None)
#        super(forms.Form, self).__init__(*args, **kwargs)
    
#        LETTER_A = 'a'
#        LETTER_B = 'b'
#        CHOICES =  ((LETTER_A, 'letter a'),
#                    (LETTER_B, 'letter b'))
        

        
        
#        height_field = forms.ChoiceField(choices=initial['choice'])
#        weight_field = forms.ChoiceField(choices=())
#        id_field = forms.ChoiceField(choices=())
#        ID_TYPES = (("si-uid", "Study instance UID"), ("acc-no", "Accession Number"))
#        id_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ID_TYPES)
    
        
#        if choice:
#            kwargs['initial']['choice'] = choice[0]
        
        
#        if choice and choice[0] not in (c[0] for c in self.CHOICES):
#            print choice
#            self.fields['choice'].choices.append(choice)
#            print self.fields['choice'].choices
