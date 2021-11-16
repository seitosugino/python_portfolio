from django.urls import path
from portfolio import views
from django.urls.conf import include

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('category/<str:category>', views.CategoryView.as_view(), name='category'),
    path('search', views.SearchView.as_view(), name='search'),
    path('address/', views.AddressEditView.as_view(), name='address'),
    path('address/new', views.AddressCreateView.as_view(), name='address_create'),
    path('app/', include('app.urls')),
]