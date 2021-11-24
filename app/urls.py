from django.urls import path
from django.urls.conf import include
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='app_index'),
    path('product/<slug>', views.ItemDetailView.as_view(), name='app_product'),
    path('additem/<slug>', views.addItem, name='app_additem'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('removeitem/<slug>', views.removeItem, name='removeitem'),
    path('removesingleitem/<slug>', views.removeSingleItem, name='removesingleitem'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('accounts/', include('accounts.urls')),
    path('search', views.SearchView.as_view(), name='app_search'),
]