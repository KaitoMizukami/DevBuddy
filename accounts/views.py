from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.views.generic import FormView, View, CreateView

from .forms import UserLoginForm, UserCreationForm


class UserLoginView(FormView):
    template_name = 'accounts/accounts_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('room:index')
        return redirect(('accounts:login'))


class UserLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


class UserRegisterView(CreateView):
    template_name = 'accounts/accounts_register.html'
    form_class = UserCreationForm
    
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('room:index')