from django import forms
from .models import Message, Room, Language


class RoomCreationForm(forms.ModelForm):
    LANGUAGES = (
        ('python', 'Python'), 
        ('php', 'PHP'), 
        ('javascript', 'Javascript'), 
        ('ruby', 'Ruby'), 
        ('go', 'Go'), 
        ('c++', 'C+++'), 
        ('typescript', 'Typescript'),
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        empty_label='言語を選択',
    )

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input'
        }
    ))

    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'textarea'
        }
    ))

    class Meta:
        model = Room
        fields = ['language', 'name', 'description']

    
class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input is-primary is-medium',
            'placeholder': 'メッセージを書いてください'
        }
    ))

    class Meta:
        model = Message
        fields = ['body']