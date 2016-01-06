from django.contrib import admin
from .models import User,Docker


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    #list_display = ('username', 'password', 'email')
    list_display = ('username', 'email')
class DockerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'describe')
admin.site.register(User,UserAdmin)
admin.site.register(Docker, DockerAdmin)