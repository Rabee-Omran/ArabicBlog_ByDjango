from datetime import datetime

from django.shortcuts import render, get_object_or_404
from .forms import NewComment, PostCreateForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from blog.models import Post, Comment
from .forms import UserCreationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .api import PostAPI, CommentsAPI
from rest_framework import viewsets
from django.contrib.auth.models import User
from blog.api import UserAPI
from django.http import Http404, HttpResponse
import http
from django.core import paginator
from django.conf.urls import url
from django.contrib.messages.api import success


def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')



    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'title': 'الصفحة الرئيسية',
        'posts': posts,
        'page': page,


    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html', {'title': 'من انا'})

def delete_own_comment(request, comment_id,post_id):
    comment = Comment.objects.get(pk=comment_id)
    post = Post.objects.get( pk=post_id )
    comment.delete()
    return redirect('detail/'+str(post_id))
    

   
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.email = request.user.email
            first_name = request.user.first_name
            last_name = request.user.last_name
            name = first_name +" "+ last_name
            new_comment.name = name
            new_comment.save()
            comment_form.is_valid = False
            comment_form = NewComment()


    else:
        comment_form = NewComment()

    context = {
        'title': post,
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'new_post.html'
    
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, 'تهانينا {} لقد تمت عملية التسجيل بنجاح.'.format(new_user))
            # messages.success(
            #     request, f'تهانينا {username} لقد تمت عملية التسجيل بنجاح . ')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {
        'title': 'التسجيل',
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        # form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.warning(request, 'هناك خطأ في اسم المستخدم او كلمة المرور')

    # else:
    #     form = LoginForm()
    return render(request, 'login.html', {
        'title': 'تسجيل الدخول',
        # 'form': form,

    })


def logout_user(request):
    logout(request)
    return render(request, 'logout.html', {
        "title": 'تسجيل الخروج'})


@login_required(login_url='login')
def profile(request):
    posts = Post.objects.filter(author=request.user)
    post_list = Post.objects.filter(author=request.user)
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'profile.html', {
        "title": "الملف الشخصي",
        "posts": posts,
        'page': page,
        'post_list': post_list,
    })


@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'تم تحديث الملف الشخصي.')
            return redirect('profile')


    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'تعديل الملف الشخصي',
        'user_form': user_form,
        'profile_form': profile_form,

    }

    return render(request, "profile_update.html", context)



#api

class Post_api(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostAPI

class User_api(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAPI

class Comments_api(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsAPI
    
