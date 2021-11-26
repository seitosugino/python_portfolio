from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    email = forms.EmailField(label='メールアドレス', max_length=100)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea())