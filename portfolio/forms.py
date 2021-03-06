from django import forms
from django.db.models.fields.files import ImageField
from .models import Category

class PostForm(forms.Form):
    category_data = Category.objects.all()
    category_choice = {}
    for category in category_data:
        category_choice[category] = category
    title = forms.CharField(max_length=30, label='タイトル')
    category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(category_choice.items()))
    content = forms.CharField(label='内容', widget=forms.Textarea())
    image = forms.ImageField(label='イメージ画像', required=False)

class AddressForm(forms.Form):
    name = forms.CharField(max_length=30)
    postal = forms.CharField(max_length=8)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=13)
    description = forms.CharField(label='自己紹介', widget=forms.Textarea(), required=False)
    image = forms.ImageField(required=False, )