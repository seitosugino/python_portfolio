from django.urls import path
from django.urls.conf import include
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/', include('accounts.urls')),
]