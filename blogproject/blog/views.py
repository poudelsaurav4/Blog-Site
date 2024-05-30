from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    blogs = Createblog.objects.order_by('-published_on')
    return render(request, 'index.html', {"blogs":blogs,})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # print("Login successful, redirecting to home")
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password")
                # print("Invalid email or password")
        except Bloguser.DoesNotExist:
            messages.error(request, "User with this email does not exist")
            # print("User with this email does not exist")
    return render(request, 'login.html')


def user_register(request):

    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
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
                Bloguser.objects.create_user(email, password, username= username, firstname = firstname, lastname= lastname, gender= gender, address = address)
                messages.success(request, "Account created successfully")
                print("-----hello created")
                return redirect('login')

    return render(request, 'register.html')

@login_required
def createblog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            images = request.FILES.get('img')

            if title and description:
                Createblog.objects.create(user = request.user, title=title, description= description, blog_img= images)
                messages.success(request, "Blog Created Successfully")
                return redirect('index')          
            else:
                messages.error(request, "Title and description should not be empty")
        return render(request, 'createblog.html') 
@login_required
@login_required
def logout_user(request):
    if request.user.is_authenticated:

        logout(request)
        messages.success(request, "You are successfully logged out")
        return render(request, 'index.html')
    
