from cProfile import label

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField

from .models import *

class AddCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'photo', 'is_published', 'cat', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }

class AddLessonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].initial = course
        self.fields['course'].widget = forms.HiddenInput()

    class Meta:
        model = Lesson
        fields = ['name', 'slug', 'description', 'content', 'video', 'is_published', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = FeedBack
        fields = ['topic', 'content', 'user', 'captcha']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'captcha': forms.TextInput(attrs={'class': 'form-input'}),
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'attempts', 'time_to_complete']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type']

class AnswerForm(forms.ModelForm):
    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)

        if question.type == 'TI':
            self.fields['is_correct'].initial = True
            self.fields['is_correct'].widget = forms.HiddenInput()

    class Meta:
        model = Answer
        fields = ['text', 'is_correct']