from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from main.decorators import only_mentors
from main.forms import CourseModelForm,ChapterFormset,TitleModelFormset,QuestionModelFormset,ChapterModelFormset, BlogModelForm, TagFormset, CommentForm, ProjectModelForm, ProjectStepFormset
from main.models import User, Courses, Chapters, Titles, Questions, Blogs, BlogLike, Tag, Comment, UserProfile, Project, Project_steps
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django import forms
from django.conf import settings
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

def all_blogs(request): #view all the blogs
    all_blogs = Blogs.objects.all()
    for blog in all_blogs:
        comments_all=Comment.objects.filter(blog=blog)
        blog.comments_all=comments_all.count()
    return render(request, "main/blog.html", {'all_blogs':all_blogs})

def post_detail(request, blog_id):
    blog=get_object_or_404(Blogs,pk=blog_id)
    user_profile = get_object_or_404(UserProfile, user=blog.author)
    # List of active comments for this post
    comments = Comment.objects.filter(blog=blog,parent=None)
    comments_all=Comment.objects.filter(blog=blog)
    new_comment = None
    comment_form = CommentForm() 
    likes=BlogLike.objects.filter(blog=blog,like=True).count()
    dislikes=BlogLike.objects.filter(blog=blog,like=False).count()
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.blog = blog
            # Save the comment to the database
            user=get_object_or_404(User, pk=request.user.id)
            new_comment.user=user
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect('post_detail', blog_id=blog.id)
    else:
            comment_form = CommentForm()
    
    return render(request, 'main/blog-single.html',{
        'blog':blog,
        'comments': comments,
        'comment_form':comment_form,
        'comments_all':comments_all,
        'user_profile':user_profile,
        'likes':likes,
        'dislikes':dislikes,
        })

def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            blog_id = request.POST.get('blog_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            blog_url = request.POST.get('blog_url')  # from hidden input
            
            reply = form.save(commit=False)
            user=get_object_or_404(User, pk=request.user.id)
            reply.user = user
            reply.blog = Blogs(id=blog_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect('post_detail', blog_id=blog_id)

    return redirect('post_detail', blog_id=blog.id)

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

def create_chapter(request,course_id):
    template_name = 'main/create_chapters.html'
    heading_message = 'Create Chapters'
    course=get_object_or_404(Courses, pk=course_id)
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = ChapterModelFormset(queryset=Chapters.objects.none())
    elif request.method == 'POST':
        formset = ChapterModelFormset(request.POST,request.FILES)
        if formset.is_valid():
            order=1
            for form in formset:                
                if form.cleaned_data.get('chapter_name'):
                    qa=form.save(commit=False)
                    qa.course=course
                    qa.order=order
                    order+=1
                    qa.save()

            return redirect('edit_courses')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })
def create_blog(request):
    template_name = 'main/create_blog.html'
    if request.method == 'GET':
        bookform = BlogModelForm(request.GET or None)
        formset = TagFormset(queryset=Tag.objects.none())
    elif request.method == 'POST':
        bookform = BlogModelForm(request.POST,request.FILES)
        formset = TagFormset(request.POST)

        if bookform.is_valid():
            course = bookform.save(commit=False)
            author=get_object_or_404(User, pk=request.user.id)
            course.author=author
            course.save()
            #tags=formset.save()
            
            #course.tags.add(*tags)
            for form in formset:
                if form.is_valid():
                    tag_name=form.cleaned_data.get('name')
                    try:
                        tag, created=Tag.objects.get_or_create(name=tag_name)
                        course.tags.add(tag)
                    except:
                        pass
                  #form.save()
            #     course.tag.append(tag)
            course.save()
            return redirect('/blog/')
    return render(request, template_name, {
        'bookform': bookform,
        'formset': formset,
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
    fields = ['title_name', 'chapter', 'description', 'order']
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
    projects=Project.objects.all()
    
    return render(request, "main/project.html", {"projects": projects})

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
            userp=UserProfile.objects.create(user=user)
            userp.save()
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
            return redirect('home') 
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'main/index.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def like_dislike_blog(request, blog_id, action):
    blog = get_object_or_404(Blogs, id=blog_id)
    user = get_object_or_404(User,id=request.user.id)
    print(user.email)
    if user==None:
        messages.error(request, "You need to sign in")
        return redirect('post_detail', blog_id=blog.id)

    if action == 'like':
        like_status = True
    elif action == 'dislike':
        like_status = False
    else:
        return redirect('blog_detail', blog_id=blog_id)
    
    try:
        like = BlogLike.objects.get(blog=blog, user=user)
        like.like = like_status
        like.save()
    except BlogLike.DoesNotExist:
        like, created = BlogLike.objects.get_or_create(blog=blog, user=user, like=like_status)
        like.like = like_status
        like.save()
    return redirect('post_detail', blog_id=blog.id)

class BlogUpdateView(UpdateView):
    model = Blogs
    template_name = 'main/course_form.html'  # Create an edit form template
    fields = ['title', 'intro','description','conclusion','tags']
    success_url = reverse_lazy('all_blogs')  # Redirect to a success page or URL after editing

def BlogDelete(request,blog_id):
        blog = get_object_or_404(Blogs, pk=blog_id)
        blog.delete()
        return redirect('all_blogs')

@only_mentors
def create_project_with_steps(request):
    template_name = 'main/create_project_with_steps.html'
    if request.method == 'GET':
        bookform = ProjectModelForm(request.GET or None)
        formset = ProjectStepFormset(queryset=Project_steps.objects.none())
    elif request.method == 'POST':
        bookform = ProjectModelForm(request.POST,request.FILES)
        formset = ProjectStepFormset(request.POST,request.FILES)
        if bookform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            project = bookform.save(commit=False);
            #mentor=User.objects.get(pk=request.user.id)
            mentor=get_object_or_404(User, pk=request.user.id)
            
            project.mentor=mentor
            if 'video' in request.FILES:
                video = request.FILES['video']
                file_extension = video.name.lower()
                if not any(file_extension.endswith(ext) for ext in settings.ALLOWED_VIDEO_EXTENSIONS):
                    messages.error(request, "Submit Valid Video!")
                    return redirect('create_project')
                content_type = video.content_type
                if content_type not in settings.ALLOWED_VIDEO_CONTENT_TYPES:
                    messages.error(request, "Submit Valid ideo!")
                    return redirect('create_project')
                
                project.video = video
            project.save()
            
            for form in formset:
                # so that `book` instance can be attached.
                project_step = form.save(commit=False)
                project_step.project = project                
                project_step.save()
            return redirect('projects')
    return render(request, template_name, {
        'bookform': bookform,
        'formset': formset,
        
    })
#themes=prism&languages=markup+css+clike+javascript+c+cpp+css-extras+django+git+go+java+kotlin+markup-templating+plsql+python+sql&plugins=line-highlight+line-numbers+custom-class+inline-color+command-line */
def project_detail(request, project_id):
    project=get_object_or_404(Project,pk=project_id)
    project_steps=Project_steps.objects.filter(project=project).order_by('order')
    user_profile = get_object_or_404(UserProfile, user=project.mentor)
    if project.code_language.upper()=='CSS':
        language='css'
    elif project.code_language.upper()=='PYTHON':
        language='python'
    elif project.code_language.upper()=='JAVASCRIPT':
        language='javascript'
    elif project.code_language.upper()=='JAVA':
        language='java'
    elif project.code_language.upper()=='KOTLIN':
        language='kotlin'
    elif project.code_language.upper()=='C++' or project.code_language.UPPER=='CPP':
        langauge='cpp'
    else:
        language=''
    if project.video:
        video_url = project.video.url
    elif project.video_url:
        video_url = project.video_url
    else:
        video_url = None
    return render(request, 'main/project_single.html',{
        'project':project,
        'project_steps': project_steps,
        'language':language,
        'user_profile':user_profile,
        'video_url': video_url,
        })
# <pre class="line-numbers">
#    <code class="language-css">
#       p { color: red }
#    </code>
# </pre>