from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from main.decorators import only_mentors
from main.forms import CourseForm, ChapterForm, TitleForm
from main.models import User,Courses,Chapters,Titles
from django import forms
#from .forms import CourseForm, ChapterForm, TitleForm
# Create your views here.
def home(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    return render(request, "main/index.html", {"fname": user_first_name})

def courses(request): #view all the courses
    user_first_name = request.session.get('user_first_name', 'Guest')
    all_courses = Courses.objects.filter(editing_status=False)
    return render(request, "main/courses.html", {"fname": user_first_name,'all_courses':all_courses})
def view_course(request,course_id):
    course= Courses.objects.get(pk=course_id)
    if course.editing_status==True:
        messages.error(request, "You do not have access to view this page!")
        return redirect('/courses')
    chapters = Chapters.objects.filter(course=course)
    return render(request, "main/course1.html", {"course":course,"chapters":chapters})

def view_chapters(request,chapter_id,course_id):
    user_first_name = request.session.get('user_first_name', 'Guest')
    course= Courses.objects.get(pk=course_id)
    if course.editing_status==True:
        messages.error(request, "You do not have access to view this page!")
        return redirect('/courses')
    chapter = Chapters.objects.get(pk=chapter_id)
    titles=Titles.objects.filter(chapter=chapter).order_by('order')
    return render(request, "main/chapter1.html", {"fname": user_first_name,"course":course,"chapter":chapter,"titles":titles})


# def view_titles(request, course_id, chapter_id):
#     user_first_name = request.session.get('user_first_name', 'Guest')
#     course = Courses.objects.get(pk=course_id)
#     chapter = get_object_or_404(Chapters, pk=chapter_id, course=course)
#     titles = Titles.objects.filter(chapter=chapter)
#     return render(request, "main/chapter_titles.html", {"fname": user_first_name, 'course': course, 'chapter': chapter, 'titles': titles})

# def title(request,course_id, chapter_id,title_id):#view 
#     user_first_name = request.session.get('user_first_name', 'Guest')
#     course = Courses.objects.get(pk=course_id)
#     chapter = get_object_or_404(Chapters, pk=chapter_id, course=course)
#     title = get_object_or_404(Titles, pk=title_id, chapter=chapter)
#     return render(request, "main/course2.html", {"fname": user_first_name,"titles":title})

# @only_mentors
# def add_course(request):
#     from django.shortcuts import render, redirect

@only_mentors
def add_course(request):
    
    if request.method == 'POST':
        
        course_form = CourseForm(request.POST, request.FILES)
        chapter_formset = forms.formset_factory(ChapterForm)(request.POST, request.FILES, prefix='chapters')
        title_formset = forms.formset_factory(TitleForm)(request.POST, request.FILES, prefix='titles')
        #print(course_form)
        if course_form.is_valid() and chapter_formset.is_valid() and title_formset.is_valid():
            # Create a new course
            course = Courses(
                course_name=course_form.cleaned_data['course_title'],
                description=course_form.cleaned_data['course_description'],
                course_picture=course_form.cleaned_data['course_image']
                # Add other fields for course model as needed
            )
            print(course)
            course.save()

            for chapter_data, title_data in zip(chapter_formset, title_formset):
                # Create chapters and titles
                chapter = Chapters(
                    chapter_name=chapter_data['chapter_title'],
                    description=chapter_data['chapter_description'],
                    chapter_picture=chapter_data['chapter_image'],
                    course=course
                    # Add other fields for chapter model as needed
                )
                chapter.save()

                title = Titles(
                    title_name=title_data['title_title'],
                    description=title_data['title_description'],
                    title_picture=title_data['title_image'],
                    chapter=chapter
                    # Add other fields for title model as needed
                )
                title.save()

            return redirect('/courses')  # Redirect to a success page
    else:
        course_form = CourseForm()
        chapter_formset = forms.formset_factory(ChapterForm)(prefix='chapters', initial=[{}])
        title_formset = forms.formset_factory(TitleForm)(prefix='titles', initial=[{}])

    return render(request, 'main/add_course.html', {
        'course_form': course_form,
        'chapter_formset': chapter_formset,
        'title_formset': title_formset
    })

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
        role = request.POST['role'] 
        if password1 == password2:
            # Create a new user
            user = User.objects.create_user( email=email,first_name=fname,last_name=lname,password=password1,role=role)
            user.save()
            messages.success(request, "User registered successfully")
            return redirect('signin')
        else:
            messages.error(request, "Passwords do not match")

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
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