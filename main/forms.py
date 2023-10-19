from django import forms
from django.forms import modelformset_factory
from main.models import Courses, Chapters, Titles
class CourseForm(forms.Form):
    course_title = forms.CharField(label='Course Title', max_length=255)

class ChapterForm(forms.Form):
    title = forms.CharField(label='Chapter Title', max_length=255)

class TitleForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ('course_name', )
        labels = {
            'course_name': 'Course Name'
        }
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Name here'
                }
            )
        }
ChapterFormset = modelformset_factory(
    Chapters,
    fields=('chapter_name', ),
    extra=1,
    widgets={
        'chapter_name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Chapter Name here'
            }
        )
    }
)
TitleModelFormset = modelformset_factory(
    Titles,
    fields=('title_name', ),
    extra=1,
    widgets={'title_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Title Name here'
        })
    }
)