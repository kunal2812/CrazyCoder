from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('courses', views.courses, name="courses"),
    path('course/<int:course_id>/',views.view_course, name="view_course"),
    path('course/<int:course_id>/<int:chapter_id>/',views.view_chapters, name="view_chapters"),
    path('project', views.projects, name="projects"),
    path('contact', views.contact, name="contact"),
    path('blog', views.blog, name="blog"),
    path('blog_single', views.blog_single, name="blog_single"),
    # path('course1', views.course1, name="course1"),
    # path('course2', views.course2, name="course2"),
    # path('course3', views.course3, name="course3"),
    #path('chapter1', views.chapter1, name="chapter1"),
    path('editcourses/',views.edit_courses,name='edit_courses'),
    path('editcourse/<int:course_id>/',views.view_course_editing,name='view_course_editing'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout, name="signout"),
    path('createcourse/',views.create_course_with_chapters,name='create_course'),
    path('add_titles/<int:course_id>/',views.create_title_model_form,name='create_title_model_form'),
    path('editcourse/<int:course_id>/<int:chapter_id/',views.mentor_view_chapter,name='view_chapters_edit')
]
