from django import forms

from .models import Post
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Enter usernmae.')

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Enter usernmae.')

    class Meta:
        model = User
        fields = ('username', 'password1')
