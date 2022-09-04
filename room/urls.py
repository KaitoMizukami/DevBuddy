from django.urls import path

from . import views


app_name = 'room'

urlpatterns = [
    path('', views.RoomIndexView.as_view(), name='index')
]