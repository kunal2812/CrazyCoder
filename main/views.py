from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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


def account(request):
    if request.method == "POST":
        action = request.POST.get('submit_action')
        if action == 'signup':
            uname = request.POST['uname']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            
            if pass1 == pass2:
                # Create a new user
                user = User.objects.create_user(username=uname, email=email, password=pass1)
                user.first_name = fname
                user.last_name = lname
                user.save()
                messages.success(request, "User registered successfully")
                return redirect('signin')  # Redirect to the login page
            else:
                messages.error(request, "Passwords do not match")

        elif action == 'signin':
            uname = request.POST['uname']
            pass1 = request.POST['pass1']
            user = authenticate(username=uname, password=pass1)
            if user is not None:
                login(request,user)
                # print(user.first_name)
                messages.success(request, "Signed in successfully")
                request.session['user_first_name'] = user.first_name
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials")
                return redirect('home')
    return render(request, 'main/index.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')