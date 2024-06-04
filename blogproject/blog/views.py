from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Q
# Create your views here.

def index(request):
    blogs = Createblog.objects.filter(blog_type= 'S')[::-1]
    paginator = Paginator(blogs, 3) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(request, 'index.html', {"blogs":blogs, "page_obj":page_obj,})

def user_login(request):
    if request.method == 'POST':
        login_input = request.POST.get('login_input')
        password = request.POST.get('password')
        user_obj = Bloguser.objects.filter(Q(email=login_input) | Q(username=login_input)).first()
        user = authenticate(request, username=user_obj, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid login details. Please try again.')

    return render(request, 'login.html')

def user_register(request):

    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        firstname = request.POST['first name']
        lastname = request.POST['last name']
        confirm_password = request.POST.get('confirm password')
        address = request.POST['address']
        gender = request.POST.get('gender')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            if Bloguser.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif Bloguser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                Bloguser.objects.create_user(email, username,password, firstname = firstname, lastname= lastname, gender= gender, address = address)
                messages.success(request, "Account created successfully")
                return redirect('login')

    return render(request, 'register.html')

@login_required
def createblog(request):
    if  not request.user.is_authenticated:
        return redirect('index')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            images = request.FILES.get('img')    
            blog_type = request.POST.get('type')
            if title and description:
                Createblog.objects.create(user = request.user, title=title, description= description, blog_type = blog_type, blog_img= images)
                messages.success(request, "Blog Created Successfully")
                return redirect('index')          
            else:
                messages.error(request, "Title and description should not be empty")
        return render(request, 'createblog.html') 

@login_required
def search_title(request):
    if  not request.user.is_authenticated:
        return redirect('index')
    elif request.method == 'POST':
        search_item = request.POST.get('search_item')
        if not search_item:
            messages.success(request, "Please Enter title to search")
            return redirect('index')
        else:
            search_results = Createblog.objects.filter(title__icontains=search_item)
            if search_results.exists():
                return render(request, 'individual.html', {"search_results": search_results})
            else:
                messages.error(request, "No blogs found with that title.")
                return redirect('index')
    else:
        return redirect('index')

@login_required
def private_blog(request):
    user = request.user
    blogs = Createblog.objects.filter(user=user).filter(blog_type = 'P')
    paginator = Paginator(blogs,5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'private.html', {'blogs': blogs, 'page_obj':page_obj})


@login_required
def my_blogs(request):
    user = request.user
    blogs = Createblog.objects.filter(user=user)
    return render(request, 'myblogs.html', {'blogs': blogs})


@login_required
def blog_details(request, pk):
    
    if  not request.user:
        return redirect('index')
    else:
        blog = get_object_or_404(Createblog, pk=pk)
        return render(request, 'details.html', {'blog':blog})

@login_required
def edit_blog(request, pk):    
    blog_edit = get_object_or_404(Createblog, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('img')
        blog_type = request.POST.get('type')
        
        if title and description:
            blog_edit.title = title
            blog_edit.description = description
            blog_edit.blog_type=blog_type
            if image:
                blog_edit.blog_img = image
            try:
                blog_edit.save()
                return redirect('details', pk=pk)
            except IntegrityError:
                return render(request, 'edit.html', {'blog_edit': blog_edit})

    return render(request, 'edit.html', {'blog_edit': blog_edit})


@login_required
def delete_blog(request, pk):
    blog_delete = get_object_or_404(Createblog, pk=pk)
    blog_delete.delete()
    messages.success(request, "Blog has successfully deleted")
    return render(request, 'index.html')

@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You are successfully logged out")
        return render(request, 'login.html')
