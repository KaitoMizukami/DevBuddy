from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, DetailView
)

from .models import Room
from .forms import RoomCreationForm


class RoomIndexView(ListView):
    template_name = 'room/room_index.html'
    model = Room


class RoomCreateView(CreateView):
    template_name = 'room/room_create.html'
    model = Room
    form_class = RoomCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('room:index')

        return render(request, 'room/room_create.html', {form: form})


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room/room_detail.html'