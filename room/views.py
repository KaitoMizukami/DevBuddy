from django.shortcuts import render
from django.views.generic import (
    ListView,
)

from .models import Room


class RoomIndexView(ListView):
    template_name = 'room/room_index.html'
    model = Room