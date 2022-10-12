from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.views.generic import (
    FormView, View, CreateView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, UserCreationForm
from .models import User


class UserLoginView(FormView):
    template_name = 'accounts/accounts_login.html'
    form_class = UserLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('room:index')
        else:
            form = UserLoginForm()
            return render(request, 'accounts/accounts_login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('room:index')
        return redirect('accounts:login')


class UserLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


class UserRegisterView(CreateView):
    template_name = 'accounts/accounts_register.html'
    form_class = UserCreationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('room:index')
        else:
            form = UserCreationForm()
            return render(request, 'accounts/accounts_register.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('room:index')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/accounts_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_rooms = context['user'].room_set.all()
        room_count = user_rooms.count()
        context['user_rooms'] = user_rooms
        context['room_count'] = room_count
        return context