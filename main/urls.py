from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CourseUpdateView, ChapterUpdateView, TitleUpdateView,BlogUpdateView
urlpatterns = [
    path('', views.home, name="home"),
    path('courses/', views.courses, name="courses"),
    path('blog/', views.all_blogs, name="all_blogs"),
    path('course/<int:course_id>/',views.view_course, name="view_course"),
    path('course/<int:course_id>/<int:chapter_id>/',views.view_chapters, name="view_chapters"),
    path('projects/', views.projects, name="projects"),
    path('contact', views.contact, name="contact"),
    # path('blog_single/<int:blog_id>/', views.view_blog, name="blog_single"),
    path('editcourses/',views.edit_courses,name='edit_courses'),
    path('editcourse/<int:course_id>/',views.view_course_editing,name='view_course_editing'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout, name="signout"),
    path('createcourse/',views.create_course_with_chapters,name='create_course'),
    path('add_titles/<int:chapter_id>/',views.create_title_model_form,name='create_title_model_form'),
    path('add_question/<int:chapter_id>/',views.create_question,name='create_question'),
    path('add_chapter/<int:course_id>/',views.create_chapter,name='create_chapter'),
    path('blog/add/',views.create_blog,name='create_blog'),
    path('editcourse/<int:course_id>/<int:chapter_id>/',views.mentor_view_chapter,name='view_chapters_edit'),
    path('publish_course/<int:course_id>/', views.publish_course, name='publish_course'),
     path('course/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('chapter/<int:pk>/edit/', ChapterUpdateView.as_view(), name='chapter_edit'),
    path('title/<int:pk>/edit/', TitleUpdateView.as_view(), name='title_edit'),
    path('course/<int:course_id>/delete/', views.CourseDelete, name='course_delete'),
    path('chapter/<int:chapter_id>/delete/', views.ChapterDelete, name='chapter_delete'),
    path('title/<int:title_id>/delete/', views.TitleDelete, name='title_delete'),
    path('blog/<int:blog_id>/',views.post_detail,name="post_detail"),
    path('comment/reply/', views.reply_page, name="reply"), #this
    path('blog/<int:pk>/editblog/', BlogUpdateView.as_view(), name='update_blog'),
    path('blog/<int:blog_id>/delete/', views.BlogDelete, name='delete_blog'),
    path('blog/<int:blog_id>/<str:action>/', views.like_dislike_blog, name='like_dislike_blog'),
    path('projects/create/',views.create_project_with_steps,name='create_project'),
    path('projects/<int:project_id>/',views.project_detail,name='project_detail'),
]