from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'input'
        }
    ))

    confirm_password = forms.CharField(label='password再入力', widget=forms.PasswordInput(
        attrs={
            'class': 'input'
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input'
        }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
    
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser' )

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', widget=forms.TextInput(
        attrs={
            'class': 'input',
            'placeholder': 'メールアドレス'
        }
    ))

    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(
        attrs={
            'class': 'input',
            'placeholder': 'パスワード'
        }
    ))

