from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from django.core.paginator import Paginator
from .models import Blog, Comment
from .forms import CommentForm
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from .utils import *


def home(request):
    return render(request,'registration/signup.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog_list')
        else:
            return redirect("login")
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.all()

    if request.GET.get('action') == 'like':
        if request.user.is_authenticated:
            if request.user in blog.likes.all():
                blog.likes.remove(request.user) 
            else:
                blog.likes.add(request.user)
        return redirect('blog_detail', pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form,
    })

def share_blog(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        notify_all_users_about_blog(title,url)
        return HttpResponse({"message":"blog send successfully"})

def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)

    return redirect('blog_detail', blog_id=blog_id)