from django.contrib import admin

from users.models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name','email','role']

admin.site.register(CustomUser, CustomUserAdmin)

