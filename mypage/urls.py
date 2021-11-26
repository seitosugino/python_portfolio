from django.urls import path
from mypage import views
from django.urls.conf import include

urlpatterns = [
    path('', views.IndexView.as_view(), name='mypage_index'),
    path('app/', include('app.urls')),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('thanks/', views.ThanksView.as_view(), name='mypage_thanks'),
]