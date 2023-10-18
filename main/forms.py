from django import forms

class CourseForm(forms.Form):
    course_title = forms.CharField(label='Course Title', max_length=255)

class ChapterForm(forms.Form):
    title = forms.CharField(label='Chapter Title', max_length=255)

class TitleForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255)