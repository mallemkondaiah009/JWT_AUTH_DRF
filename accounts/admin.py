from django.contrib import admin
from .models import User

class AdminUser(admin.ModelAdmin):
    list_display = ['id','username','email','password','is_active','created_at']

admin.site.register(User, AdminUser)

