# This file is Copyright 2010 John Boxall
# The original version can be found at
# https://gist.github.com/johnboxall/396540

import django_filters
from django import forms

class DateRangeField(django_filters.fields.RangeField):
    # Django-Filter DateRangeFilter that really accepts a range of dates ;)
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(),
            forms.DateField(widget=forms.TextInput(attrs={'class':'date'})),
        )
        forms.MultiValueField.__init__(self, fields, *args, **kwargs)

class DateRangeFilter(django_filters.RangeFilter):
    field_class = DateRangeField
