from django.urls import path
from django.urls.conf import include
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='app_index'),
    path('product/<slug>', views.ItemDetailView.as_view(), name='app_product'),
    path('accounts/', include('accounts.urls')),
]