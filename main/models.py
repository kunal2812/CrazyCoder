from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    title_pictire=models.ImageField(null=True,upload_to='images/Titles')
    order = models.FloatField()

    def __str__(self):
        return self.title_name

class Questions(models.Model):
    chapter=models.ForeignKey(Chapters, on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    def __str__(self):
        return self.question