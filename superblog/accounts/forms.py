from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from blog.models import Author, Post
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField



class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(label='никнейм', help_text='максимум 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AuthorUpdateForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'author_photo', 'about']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}, ),
        }

class PostForm(forms.ModelForm):

    tags_str = forms.CharField(help_text='Пример: тег1, тег2, тег3', label='добавление тегов',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='капча')

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'category', 'tags_str', 'captcha']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),

            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7, }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

