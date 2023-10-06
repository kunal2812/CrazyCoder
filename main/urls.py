from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('courses', views.courses, name="courses"),
    path('project', views.projects, name="projects"),
    path('contact', views.contact, name="contact"),
    path('blog', views.blog, name="blog"),
    path('blog_single', views.blog_single, name="blog_single"),
    path('course1', views.course1, name="course1"),
    path('course2', views.course2, name="course2"),
    path('course3', views.course3, name="course3"),
    path('account', views.account, name="account"),
    path('signout', views.signout, name="signout"),
]
