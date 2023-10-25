from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CourseUpdateView, ChapterUpdateView, TitleUpdateView
urlpatterns = [
    path('', views.home, name="home"),
    path('courses/', views.courses, name="courses"),
    path('all_blogs/', views.all_blogs, name="all_blogs"),
    path('course/<int:course_id>/',views.view_course, name="view_course"),
    path('course/<int:course_id>/<int:chapter_id>/',views.view_chapters, name="view_chapters"),
    path('project', views.projects, name="projects"),
    path('contact', views.contact, name="contact"),
    path('blog', views.blog, name="blog"),
    path('blog_single/<int:blog_id>/', views.view_blog, name="blog_single"),
    path('editcourses/',views.edit_courses,name='edit_courses'),
    path('editcourse/<int:course_id>/',views.view_course_editing,name='view_course_editing'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout, name="signout"),
    path('createcourse/',views.create_course_with_chapters,name='create_course'),
    path('add_titles/<int:chapter_id>/',views.create_title_model_form,name='create_title_model_form'),
    path('add_question/<int:chapter_id>/',views.create_question,name='create_question'),
    path('add_chapter/<int:course_id>/',views.create_chapter,name='create_chapter'),
    path('add_blog/',views.create_blog,name='create_blog'),
    path('editcourse/<int:course_id>/<int:chapter_id>/',views.mentor_view_chapter,name='view_chapters_edit'),
    path('publish_course/<int:course_id>/', views.publish_course, name='publish_course'),
     path('course/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('chapter/<int:pk>/edit/', ChapterUpdateView.as_view(), name='chapter_edit'),
    path('title/<int:pk>/edit/', TitleUpdateView.as_view(), name='title_edit'),
    path('course/<int:course_id>/delete/', views.CourseDelete, name='course_delete'),
    path('chapter/<int:chapter_id>/delete/', views.ChapterDelete, name='chapter_delete'),
    path('title/<int:title_id>/delete/', views.TitleDelete, name='title_delete'),
]