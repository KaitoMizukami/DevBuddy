from django.urls import path

from . import views


app_name = 'room'

urlpatterns = [
    path('', views.RoomIndexView.as_view(), name='index'),
    path('room/create', views.RoomCreateView.as_view(), name='create'),
    path('room/detail/<int:pk>/', views.room_detail_view, name='detail'),
    path('room/update/<int:pk>/', views.RoomUpdateView.as_view(), name='update'),
    path('room/delete/<int:pk>/', views.RoomDeleteView.as_view(), name='delete'),
]