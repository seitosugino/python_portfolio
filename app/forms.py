from django import forms

class OrderForm(forms.Form):
    postal = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)