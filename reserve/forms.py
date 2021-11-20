from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    tel = forms.CharField(label='電話番号', max_length=100)
    remarks = forms.CharField(label='備考', widget=forms.Textarea())