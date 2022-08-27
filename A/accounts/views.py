from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm, LoginForm
from .models import OtpCode, User
from utils import send_otp_code
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import random


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(phone_number=form.cleaned_data['phone_number'], code=random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a verify code!', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {"form": form})


class UserVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        form = self.form_class(request.POST)
        otp_code = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == otp_code.code:
                User.objects.create_user(phone_number=otp_code.phone_number, email=user_session['email'],
                                         full_name=user_session['full_name'], password=user_session['password'])
                otp_code.delete()
                messages.success(request, 'You registered successfully!', 'success')
            else:
                messages.error(request, 'Your code is wrong!', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'login successfully!', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'username or password is wrong!', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout successfully!', 'success')
        return redirect('home:home')
