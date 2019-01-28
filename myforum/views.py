from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm
from .forms import LoginForm
from .forms import CommentForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import pandas as pd
import datetime as dt
import csv
import nltk
#nltk.download('punkt')
from nltk import sent_tokenize
import re


import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
from sklearn.feature_selection import chi2


import numpy as np
from sklearn import linear_model
from sklearn.metrics import precision_score, recall_score, accuracy_score, log_loss, classification_report
import xgboost as xgb
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
import pickle


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    users = User.objects.all()
    msg_blocks = {'posts': posts, 'users': users}
    return render(request, 'myforum/post_list.html', msg_blocks)

def profile_detail(request, pk):
    user = get_object_or_404(User, pk = pk)
    return render(request, 'myforum/profile_detail.html', 'user':user)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    sum_post = gensim_summarize(post.text)
    comments = post.comments.order_by('-created_date')
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
    msg_blocks = {'post': post, 'form': form, 'comments':comments, 'sum':sum_post}
    return render(request, 'myforum/post_detail.html', msg_blocks)

def comment_edit(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(instance=comment)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            attack_prob = "no"
            post = form.save(commit=False)
            post_body = form.cleaned_data.get('text')

            n = attack_probability(post_body)
            if(n[0]>0.5):
                attack_prob = "yes"
                msg_blocks = {'form': form, 'attack_prob':attack_prob}
                return render(request, 'myforum/post_new.html', msg_blocks)
            else:
                attack_prob = "no"
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
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = post.published_date
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        heading = "Edit Post"
    msg_blocks = {'form': form, 'heading':heading}
    return render(request, 'myforum/post_new.html', msg_blocks)

def gensim_summarize(article_text):
    #sentence =  sent_tokenize(article_text)
    sentence = re.split(r' *[\.\?!][\'"\)\]]* *', article_text)
    #sentence =  article_text.split(',.')
    # for i in sentence:
    #     print(i+" #####new####")
    if(len(sentence)>10):
        print("\nlength: ", len(sentence))
        print("original text: \n", article_text)
        print("\nsummarize text: \n", summarize(article_text), "\n")
        return summarize(article_text, ratio=0.2)
        #return summarize(article_text, word_count=50)

def attack_probability(article_text):
    file_name = "EdwardDixon_data/attack_train.csv"

    raw_samples = pd.read_csv(file_name)
    vectorizer = CountVectorizer(lowercase=True,stop_words='english')
    X_counts = vectorizer.fit_transform(raw_samples["comment"])

    # We need to be able to lookup counts for a given word.  We'll make a dictionary to help with that
    #word_to_feature_index = dict(zip(vectorizer.get_feature_names(), range(0, len(vectorizer.get_feature_names()))))

    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_counts)

    loaded_model = pickle.load(open("best_xgb.mdl", 'rb'))

    text_clf = Pipeline([('vect', vectorizer),
                      ('tfidf', tfidf_transformer),
                      ('clf', loaded_model)])
    test = []
    test.append(article_text)
    print(text_clf.predict_proba(test)[:,1])
    is_attack = text_clf.predict_proba(test)[:,1]
    #print(text_clf.predict_proba(test)[:,1])
    return is_attack
