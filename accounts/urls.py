from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.UserRegisterView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.UserProfile.as_view(), name="profile"),
]