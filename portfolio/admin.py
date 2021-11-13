from django.contrib import admin
from .models import Post, Category, Address

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Address)