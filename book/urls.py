from django.urls import path
from book import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='book_index'),
    path('detail/<str:isbn>', views.DetailView.as_view(), name='book_detail'),
]