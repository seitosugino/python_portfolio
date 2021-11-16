from django.shortcuts import render, redirect
from allauth.account import views
from django.urls.base import is_valid_path
from django.views import View
from django.contrib.auth.models import User
from accounts.forms import ProfileForm
from portfolio.models import Address

class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')

class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)
        address_data = Address.objects.filter(author=request.user)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'address_data': address_data,
        })

class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial = {
                'last_name': user_data.last_name,
                'first_name': user_data.first_name,
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = User.objects.get(id=request.user.id)
            user_data.last_name = form.cleaned_data['last_name']
            user_data.first_name = form.cleaned_data['first_name']
            user_data.save()
            return redirect('account_profile')
        return render(request, 'accounts/profile.html', {
            'form': form
        })