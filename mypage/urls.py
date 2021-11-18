from django.urls import path
from mypage import views
from django.urls.conf import include

urlpatterns = [
    path('', views.IndexView.as_view(), name='mypage_index'),
    path('app/', include('app.urls')),
]