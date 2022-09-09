from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Room, Language, Message
from .forms import RoomCreationForm, MessageForm


class RoomIndexView(ListView):
    template_name = 'room/room_index.html'
    model = Room

    def get_queryset(self):
        query_word = self.request.GET.get('query')
        if query_word:
            object_list = Room.objects.filter(
                Q(language__name__icontains=query_word) |
                Q(name__icontains=query_word) |
                Q(description__icontains=query_word)
            )
        else:
            object_list = Room.objects.all()

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        languages = Language.objects.all()
        room_count = self.object_list.count()
        three_recent_msgs = Message.objects.all().order_by('-created_at')[:3]
        context['languages'] = languages
        context['room_count'] = room_count
        context['three_recent_msgs'] = three_recent_msgs
        return context


class RoomCreateView(LoginRequiredMixin ,CreateView):
    template_name = 'room/room_create.html'
    model = Room
    form_class = RoomCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            room.participants.add(request.user)
            return redirect('room:index')

        return render(request, 'room/room_create.html', {form: form})


def room_detail_view(request, pk):
    room = Room.objects.get(id=pk)
    room_participants = room.participants.all()
    messages = room.message_set.all()
    message_count = messages.count()
    languages = Language.objects.all()
    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.user = request.user
        message.room = room
        message.save()
        if request.user not in room_participants:
            room.participants.add(request.user)
        return redirect('room:detail', pk=room.id)

    context = {'form': form, 'languages': languages,
               'room': room, 'room_messages': messages,
               'message_count': message_count, 'room_participants': room_participants}
    return render(request, 'room/room_detail.html', context)


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'room/room_update.html'
    form_class = RoomCreationForm
    success_url = reverse_lazy('room:index')


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'room/room_delete.html'
    success_url = reverse_lazy('room:index')
