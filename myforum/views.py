from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .forms import LoginForm
from .forms import CommentForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myforum/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    msg_blocks = {'post': post, 'form': form}
    return render(request, 'myforum/post_detail.html', msg_blocks)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myforum/post_new.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile.joined_date = timezone.now()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'myforum/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'myforum/login.html', {'form': form})

    # if request.method == "POST":
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         u_username = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         user = authenticate(username=u_username, password=raw_password)
    #         login(request, user)
    #         return redirect('post_list')
    # else:
    #     form = LoginForm()
    # return render(request, 'myforum/login.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = SignUpForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myforum/post_new.html', {'form': form})
