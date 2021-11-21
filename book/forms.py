from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=200, required=True)