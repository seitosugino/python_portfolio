from django import forms

class ProfileForm(forms.Form):
    last_name = forms.CharField(max_length=30, label='姓')
    first_name = forms.CharField(max_length=30, label='名')