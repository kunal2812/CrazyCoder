from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from main.decorators import only_mentors
from main.forms import CourseModelForm,ChapterFormset,TitleModelFormset,QuestionModelFormset
from main.models import User,Courses,Chapters,Titles, Questions
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django import forms
#from .forms import CourseForm, ChapterForm, TitleForm
# Create your views here.
def home(request):
    user_first_name = request.session.get('user_first_name', 'Guest')
    courses = Courses.objects.filter(editing_status=False)
    return render(request, "main/index.html", {"fname": user_first_name,'courses':courses})

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
    questions=Questions.objects.filter(chapter=chapter)
    return render(request, "main/chapter1.html", {"fname": user_first_name,"course":course,"chapter":chapter,"titles":titles,"questions":questions})


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
def edit_courses(request): #view all the courses
    user_first_name = request.session.get('user_first_name', 'Guest')
    mentor=User.objects.get(pk=request.user.id)
    all_courses = Courses.objects.filter(editing_status=True,mentor=mentor)
    return render(request, "main/mentor_courses.html", {"fname": user_first_name,'all_courses':all_courses})

@only_mentors
def view_course_editing(request,course_id):
    if request.method == 'POST':
        pass
    course= Courses.objects.get(pk=course_id)
    if (request.user.id!=course.mentor.id):
        messages.error(request, "You do not have access to view this page!")
        return redirect('/')
    chapters = Chapters.objects.filter(course=course)
    return render(request, "main/edit_course.html", {"course":course,"chapters":chapters})

@only_mentors        
def mentor_view_chapter(request,chapter_id,course_id):
    
    user_first_name = request.session.get('user_first_name', 'Guest')
    course= Courses.objects.get(pk=course_id)
    chapter = Chapters.objects.get(pk=chapter_id)
    titles=Titles.objects.filter(chapter=chapter).order_by('order')
    questions=Questions.objects.filter(chapter=chapter)
    return render(request, "main/mentor_view_chapter.html", {"fname": user_first_name,"course":course,"chapter":chapter,"titles":titles,"questions":questions})

@only_mentors
def create_course_with_chapters(request):
    template_name = 'main/create_course_with_chapters.html'
    if request.method == 'GET':
        bookform = CourseModelForm(request.GET or None)
        formset = ChapterFormset(queryset=Chapters.objects.none())
    elif request.method == 'POST':
        bookform = CourseModelForm(request.POST,request.FILES)
        formset = ChapterFormset(request.POST,request.FILES)
        if bookform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            course = bookform.save(commit=False);
            #mentor=User.objects.get(pk=request.user.id)
            mentor=get_object_or_404(User, pk=request.user.id)
            
            course.mentor=mentor
            course.save()
            order=1
            for form in formset:
                # so that `book` instance can be attached.
                chapter = form.save(commit=False)
                chapter.course = course
                chapter.order=order
                order+=1
                chapter.save()
            return redirect('edit_courses')
    return render(request, template_name, {
        'bookform': bookform,
        'formset': formset,
    })

def create_title_model_form(request,chapter_id):
    template_name = 'main/create_titles.html'
    heading_message = 'Create Titles'
    chapter=get_object_or_404(Chapters, pk=chapter_id)
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = TitleModelFormset(queryset=Titles.objects.none())
    elif request.method == 'POST':
        formset = TitleModelFormset(request.POST,request.FILES)
        if formset.is_valid():
            order=1
            for form in formset:                
                if form.cleaned_data.get('title_name'):
                    title=form.save(commit=False)
                    title.chapter=chapter
                    title.order=order
                    order+=1
                    title.save()

            return redirect('edit_courses')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })
def create_question(request,chapter_id):
    template_name = 'main/create_questions.html'
    heading_message = 'Create Questions'
    chapter=get_object_or_404(Chapters, pk=chapter_id)
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = QuestionModelFormset(queryset=Questions.objects.none())
    elif request.method == 'POST':
        formset = QuestionModelFormset(request.POST,request.FILES)
        if formset.is_valid():
            order=1
            for form in formset:                
                if form.cleaned_data.get('question'):
                    qa=form.save(commit=False)
                    qa.chapter=chapter
                    qa.save()

            return redirect('edit_courses')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })

def publish_course(request, course_id):
    # Get the course object
    course = get_object_or_404(Courses, pk=course_id)

    # Check if the user is authorized to publish the course
    if request.user == course.mentor:
        # Set the editing_status to False and save the course
        course.editing_status = False
        course.save()
        
        # Display a success message (optional)
        messages.success(request, 'Course published successfully.')

        return redirect('edit_courses')  # Redirect to course detail view
    else:
        # Display an error message for unauthorized access (optional)
        messages.error(request, 'You do not have permission to publish this course.')
        return redirect('edit_courses')  # Redirect to course detail view with an error message

class CourseUpdateView(UpdateView):
    model = Courses
    template_name = 'main/course_form.html'  # Create an edit form template
    fields = ['course_name', 'mentor', 'description', 'course_pictire', 'course_language', 'editing_status']
    success_url = reverse_lazy('edit_courses')  # Redirect to a success page or URL after editing

# Edit Chapter View
class ChapterUpdateView(UpdateView):
    model = Chapters
    template_name = 'main/course_form.html'  # Create an edit form template
    fields = ['chapter_name', 'course', 'description', 'chapter_pictire', 'order']
    success_url = reverse_lazy('edit_courses')  # Redirect to a success page or URL after editing

# Edit Title View
class TitleUpdateView(UpdateView):
    model = Titles
    template_name = 'main/course_form.html'  # Create an edit form template
    fields = ['title_name', 'chapter', 'description', 'title_picture', 'order']
    success_url = reverse_lazy('edit_courses')  # Redirect to a success page or URL after editing


def CourseDelete(request,course_id):
        course = get_object_or_404(Courses, pk=course_id)
        course.delete()
        return redirect('edit_courses')
def ChapterDelete(request,chapter_id):
        chapter = get_object_or_404(Chapters, pk=chapter_id)
        chapter.delete()
        return redirect('edit_courses')
def TitleDelete(request,title_id):
        title = get_object_or_404(Titles, pk=title_id)
        title.delete()
        return redirect('edit_courses')

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