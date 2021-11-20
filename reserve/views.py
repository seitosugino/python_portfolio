from django.core.exceptions import SynchronousOnlyOperation
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from .models import Booking, Store, Staff
from portfolio.models import Address
from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.utils.timezone import localtime, make_aware
from reserve.forms import BookingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
          start_date = date.today()
          weekday = start_date.weekday()
          if weekday != 6:
              start_date = start_date - timedelta(days=weekday + 1)
          return redirect('reserve_my_page', start_date.year, start_date.month, start_date.day)

        store_data = Store.objects.all()

        return render(request, 'reserve/index.html', {
            'store_data': store_data
        })

class StaffView(View):
    def get(self, request, *args, **kwargs):
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        staff_data = Staff.objects.filter(store=store_data).select_related('address')
        address_data = Address.objects.all()

        return render(request, 'reserve/staff.html', {
            'store_data': store_data,
            'staff_data': staff_data,
            'address_data': address_data
        })

class CalendarView(View):
    def get(self, request, *args, **kwargs):
        staff_data = Staff.objects.filter(id=self.kwargs['pk']).select_related('address').select_related('store')[0]
        today = date.today()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            start_date = date(year=year, month=month, day=day)
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        for hour in range(10,21):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=10, minute=0, second=0)))
        booking_data = Booking.objects.filter(staff=staff_data).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_data = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_data in calendar[booking_hour]):
                calendar[booking_hour][booking_data] = False

        return render(request, 'reserve/calendar.html', {
            'staff_data': staff_data,
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today
        })

class BookingView(View):
    def get(self, request, *args, **kwargs):
        staff_data = Staff.objects.filter(id=self.kwargs['pk']).select_related('address').select_related('store')[0]
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form = BookingForm(request.POST or None)

        return render(request, 'reserve/booking.html', {
            'staff_data': staff_data,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form
        })

    def post(self, request, *args, **kwargs):
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
        booking_data = Booking.objects.filter(staff=staff_data,start=start_time)
        form = BookingForm(request.POST or None)
        if booking_data.exists():
            form.add_error(None, '既に予約がございます。\n別の日程で予約をお願い致します。')
        else:
            if form.is_valid():
                booking = Booking()
                booking_staff = staff_data
                booking_start = start_time
                booking.end = end_time
                booking.name = form.cleaned_data['name']
                booking.tel = form.cleaned_data['tel']
                booking.remarks = form.cleaned_data['remarks']
                booking.save()
                return redirect('reserve_thanks')

        return render(request, 'reserve/booking.html', {
            'staff_data': staff_data,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form
        })

class ThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reserve/thanks.html')

class MyPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        staff_data = Staff.objects.filter(id=request.user.id).select_related('address').select_related('store')[0]
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        start_date = date(year=year, month=month, day=day)
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        for hour in range(10,21):
            row = {}
            for day_ in days:
                row[day_] = ''
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=10, minute=0, second=0)))
        booking_data = Booking.objects.filter(staff=staff_data).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_data = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_data in calendar[booking_hour]):
                calendar[booking_hour][booking_data] = booking.name

        return render(request, 'reserve/my_page.html', {
            'staff_data': staff_data,
            'booking_data': booking_data,
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'year': year,
            'month': month,
            'day': day
        })

@require_POST
def Holiday(request, year, month, day, hour):
    staff_data = Staff.objects.get(id=request.user.id)
    start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
    end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))

    Booking.objects.create(
        staff=staff_data,
        start=start_time,
        end=end_time
    )

    start_date = date(year=year, month=month, day=day)
    weekday = start_date.weekday()
    if weekday != 6:
        start_date = start_date - timedelta(days=weekday + 1)
    return redirect('reserve_my_page', year=start_date.year, month=start_date.month, day=start_date.day)