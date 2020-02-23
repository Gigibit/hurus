from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from djangoql.admin import DjangoQLSearchMixin
'''

DjangoQL is shipped with comprehensive Syntax Help, which can be found in Django admin (see the Syntax Help link in auto-completion popup). Here's a quick summary:

DjangoQL's syntax resembles Python's, with some minor differences. Basically you just reference model fields as you would in Python code, then apply comparison and logical operators and parenthesis. DjangoQL is case-sensitive.

model fields: exactly as they are defined in Python code. Access nested properties via ., for example author.last_name;
strings must be double-quoted. Single quotes are not supported. To escape a double quote use \";
boolean and null values: True, False, None. Please note that they can be combined only with equality operators, so you can write published = False or date_published = None, but published > False will cause an error;
logical operators: and, or;
comparison operators: =, !=, <, <=, >, >= - work as you expect. ~ and !~ - test whether or not a string contains a substring (translated into __icontains);
test a value vs. list: in, not in. Example: pk in (2, 3).

example to search by field a course:

language = "IT"

'''


admin.site.site_header = 'HelloCurus Admin Console'

@admin.register(Employee)
class EmployeeProfileAdmin(admin.ModelAdmin):
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'agency')}),
          ('Employee info' , {'fields': ('team',)}),
        )
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            }),
        )
    list_display = ('email', 'first_name', 'last_name', 'agency', 'team')
    search_fields = ('email', 'first_name', 'last_name','agency__name', 'team__name')
    ordering = ('email',)

@admin.register(Manager)
class ManagerProfileAdmin(admin.ModelAdmin):
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'agency')}),
        )
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2','agency'),
            }),
        )
    list_display = ('email', 'first_name', 'last_name', 'agency')
    search_fields = ('email', 'first_name', 'last_name','agency__name')
    ordering = ('email',)

@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    exclude = ('title',)
    list_display = ('title', 'course')
    search_fields = ('title', 'course')


@admin.register(EncouragingSentence)
class EncouragingSentenceAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('text', 'author', 'language')
    search_fields = ('text', 'author', 'language')



@admin.register(Course)
class CourseSentenceAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('title', 'description', 'language')
    search_fields = ('title', 'description','language')






admin.site.unregister(Group)

admin.site.register(Team)
admin.site.register(Agency)
admin.site.register(Curus)

