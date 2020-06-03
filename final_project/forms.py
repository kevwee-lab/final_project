from django import forms

class FilterForm(forms.Form):
    from_year = forms.IntegerField()
    to_year = forms.IntegerField()