from django.urls import path
from reserve import views
from django.urls.conf import include

urlpatterns = [
    path('', views.IndexView.as_view(), name='reserve_index'),
    path('store/<int:pk>', views.StaffView.as_view(), name='staff'),
    path('calendar/<int:pk>', views.CalendarView.as_view(), name='calendar'),
    path('calendar/<int:pk>/<int:year>/<int:month>/<int:day>', views.CalendarView.as_view(), name='calendar'),
    path('Booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>', views.BookingView.as_view(), name='booking'),
    path('thanks', views.ThanksView.as_view(), name='reserve_thanks'),
    path('my_page/<int:year>/<int:month>/<int:day>', views.MyPageView.as_view(), name='reserve_my_page'),
    path('my_page/holiday/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Holiday, name='holiday'),
]