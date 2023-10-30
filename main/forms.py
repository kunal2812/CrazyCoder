from django import forms
from django.forms import modelformset_factory
from main.models import Courses, Chapters, Titles, Questions, Blogs, Tag, Comment
class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ('course_name', 'description', 'course_pictire', 'course_language')
        labels = {
            'course_name': 'Course Name',
            'description': 'Description',
            'course_pictire': 'Course Picture',
            'course_language': 'Course Language',
        }
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Name here'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Description here'
            }),
            'course_pictire': forms.FileInput(attrs={
                'class': 'form-control-file',
                'required':False,
                'label': 'Title Thumbnail'
            }),
            'course_language': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Language here'
            }),
        }
ChapterFormset = modelformset_factory(
    Chapters,
    fields=('chapter_name','description','chapter_pictire' ),
    extra=1,
    widgets={
        'chapter_name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Chapter Name here'
            }),
        'description': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Chapter Description here'
            }),
        'chapter_pictire': forms.FileInput(attrs={
            'class': 'form-control-file',
            'label': 'Title Thumbnail'  # Add this line to set the label
        }),
    }
)
TitleModelFormset = modelformset_factory(
    Titles,
    fields=('title_name','description'),
    extra=1,
    widgets={'title_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Title Name here'
        }),
        'description': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Title Description here'
        }),
    }
    
)

QuestionModelFormset = modelformset_factory(
    Questions,
    fields=('question','answer'),
    extra=1,
    widgets={'question': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Question here'
        }),
        'answer': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Answer here'
        }),
    }
)

ChapterModelFormset = modelformset_factory(
    Chapters,
    fields=('chapter_name','description','chapter_pictire'),
    extra=1,
    widgets={'chapter_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Chapter Name here'
        }),
        'description': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Chapter Description here'
        }),
        'chapter_pictire': forms.FileInput(attrs={
            'class': 'form-control-file',
            'label': 'Chapter Thumbnail'  # Add this line to set the label
        }),
    }
    
)

class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('title', 'intro','description','conclusion', 'blog_picture')
        labels = {
            'title': 'Title',
            'intro':'Introduction',
            'description': 'Description',
            'conclusion': 'Conclusion',
            'blog_pictire': 'Blog Thumbnail',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title Name here'
            }),
            'intro': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Blog Introduction here'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Blog Description here'
            }),
            'conclusion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Blog Conclusion here'
            }),
            'blog_picture': forms.FileInput(attrs={
                'class': 'form-control-file',
                'required':False,
                'label': 'Blog Thumbnail'
            }),
        }
TagFormset = modelformset_factory(
    Tag,
    fields=('name', ),
    extra=1,
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Tag'
            }),
    }
)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('message',)
    #overidrinding defalut form setting and adding bootstrap
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs={'placeholder': 'Write your comment','class':'form-control'}
