from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""
    ROLE=(('Student','STUDENT'),('Mentor','MENTOR'))
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role=models.CharField(choices=ROLE,max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Courses(models.Model):
    course_name=models.CharField(max_length=100,blank=False)
    mentor= models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()
    course_pictire=models.ImageField(null=True,upload_to='images/Courses/')
    course_language=models.CharField(max_length=50)
    editing_status=models.BooleanField(default=True,blank=False);

    def __str__(self):
        return self.course_name

class Chapters(models.Model):
    chapter_name=models.CharField(max_length=100,blank=False)
    course= models.ForeignKey(Courses,on_delete=models.CASCADE)
    description=models.TextField()
    chapter_pictire=models.ImageField(null=True,upload_to='images/Chapters/')
    order = models.FloatField()
    

    def __str__(self):
        return self.chapter_name
class Titles(models.Model):
    title_name=models.CharField(max_length=100,blank=False)
    chapter= models.ForeignKey(Chapters,on_delete=models.CASCADE)
    description=models.TextField()
    order = models.FloatField()

    def __str__(self):
        return self.title_name

class Questions(models.Model):
    chapter=models.ForeignKey(Chapters, on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    def __str__(self):
        return self.question
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name    
class Blogs(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=False)
    intro=models.TextField()
    description=models.TextField()
    conclusion=models.TextField()
    blog_picture=models.ImageField(null=True,upload_to='image/blog/')
    tags=models.ManyToManyField(Tag,related_name='Blogs',blank=True)
    created_at=models.DateTimeField(default=timezone.now)
    def get_comments(self):
        return self.comments.filter(parent=None)
    def save(self, *args, **kwargs):
        # Set the 'created_at' field to the current local time
        if not self.created_at:
            self.created_at = timezone.now()
        super(Blogs, self).save(*args, **kwargs)
    def __str__(self):
        return self.title
    
class BlogLike(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    like=models.BooleanField(default=None)

    class Meta:
        unique_together = ['blog','user']
    def __str__(self):
        return f'{self.user} {"liked" if self.like else "disliked"} {self.blog}'
    
class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE,related_name="comments")  # Add this field
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('timestamp',)
    def get_comments(self):
        return Comment.objects.filter(parent=self)
    def __str__(self):
        return f'Comment by {self.user.email} on {self.timestamp}'
    
class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='userprofiles')
    profile_picture=models.ImageField(null=True,default='defaultpic.jpg',upload_to='image/profile')
    bio=models.TextField(default='I am passionate about learning!')

    def __str__(self):
        return f'{self.user.first_name}'
    
class Project(models.Model):
    CODE_LANGUAGE_CHOICES = [
        ('Css','CSS'),
        ('html','HTML'),
        ('javascript','Javascript'),
        ('python','Python'),
        ('kotlin','Kotlin'),
        ('java','Java'),
    ]
    mentor=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=60)
    picture=models.ImageField(default='project.png',upload_to='image/project')
    video = models.FileField(upload_to='image/videos/', null=True, blank=True, help_text="Upload a video file (or)")
    video_url = models.URLField(null=True, blank=True, help_text="Enter a video URL (or)")
    intro=models.TextField()
    conclusion=models.TextField()
    code=models.TextField(null=True)
    code_language=models.CharField(max_length=20,null=True,choices=CODE_LANGUAGE_CHOICES)
    def __str__(self):
        return f'{self.title}'

class Project_steps(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='project_steps')
    order=models.IntegerField()
    text=models.TextField()
    picture=models.ImageField(null=True,blank=True,upload_to='image/project/')
    def __str__(self):
        return f'{self.order } {self.project.title}'
