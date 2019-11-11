from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group



admin.site.site_header = 'HelloCurus Admin Console'

@admin.register(Employee)
class EmployeeProfileAdmin(admin.ModelAdmin):
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'password')}),
          ('Employee info' , {'fields': ('team',)}),
        )
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            }),
        )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Manager)
class ManagerProfileAdmin(admin.ModelAdmin):
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'password')}),
        )
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            }),
        )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.unregister(Group)

admin.site.register(Team)
admin.site.register(Tought)
admin.site.register(Agency)

