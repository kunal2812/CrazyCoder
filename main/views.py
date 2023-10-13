from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from main.models import User
# Create your views here.
def home(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/index.html", {"fname": user_first_name})

def courses(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/courses.html", {"fname": user_first_name})

def course1(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/course1.html", {"fname": user_first_name})

def course2(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/course2.html", {"fname": user_first_name})

def course3(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/course3.html", {"fname": user_first_name})

def chapter1(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/chapter1.html", {"fname": user_first_name})

def projects(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/project.html", {"fname": user_first_name})

def blog(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/blog.html", {"fname": user_first_name})

def blog_single(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/blog-single.html", {"fname": user_first_name})


def contact(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/contact.html", {"fname": user_first_name})



def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1= request.POST['pass1']
        password2= request.POST['pass2']
        role = request.POST.get('role', 'student') 
        if password1 == password2:
            # Create a new user
            user = User.objects.create_user( email=email,first_name=fname,last_name=lname,password=password1)
            user.save()
            messages.success(request, "User registered successfully")
            return redirect('signin')
        else:
            messages.error(request, "Passwords do not match")

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        # user = authenticate(request, username=username, password=password)
        user = authenticate(request,email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Signed in successfully")
            request.session['user_first_name'] = user.username
            # print(f"User's first name: {user.username}")
            # print(f"User's role: {user.role}")
            return redirect('home') 
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'main/index.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')