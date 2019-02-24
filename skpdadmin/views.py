from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('myapp.home_urls:homepage'))
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return HttpResponseRedirect(reverse('myapp.home_urls:homepage'))
            else:
                return render(request, 'registration/login.html', {'form': form})
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('myapp.home_urls:homepage'))
    else:
        return HttpResponseRedirect(reverse('custom_login'))
