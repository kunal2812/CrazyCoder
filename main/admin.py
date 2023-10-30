
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Courses, Chapters, Titles, Tag, Blogs, Comment, UserProfile, BlogLike
admin.site.register(Courses)
admin.site.register(Chapters)
admin.site.register(Titles)
admin.site.register(Tag)
admin.site.register(Blogs)
admin.site.register(UserProfile)
admin.site.register(BlogLike)
@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff','role')
    search_fields = ('email', 'first_name', 'last_name','role')
    ordering = ('email',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user', 'blog', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('message',)