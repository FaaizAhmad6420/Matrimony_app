from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .models import CustomUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verification_token = str(uuid.uuid4())
            user.save()

            current_site = get_current_site(request)
            subject = "Activate Your Account"
            activation_link = f"http://{current_site}/accounts/verify_email/{user.email_verification_token}/"
            message = f"Click the link to activate your account: {activation_link}"
            send_mail(subject, message, "66testing99@gmail.com", [user.email])

            return redirect('accounts:login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        if user:
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()

            return redirect('accounts:login')

    except:
        return HttpResponse('Activation link is Invalid')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_email_verified:
                login(request, user)
                return redirect('matrimony:profile_list')
            else:
                return redirect('accounts:login')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('matrimony:profile_list')


def delete_view(request):
    request.user.delete()
    messages.success(request, 'Your Account has been deleted successfully')
    return redirect('accounts:login')
