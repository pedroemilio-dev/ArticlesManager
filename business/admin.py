from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, UserProfile

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ()}),  
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'createdAt', 'public')  
    list_filter = ('public', 'createdAt')  
    search_fields = ('title', 'description', 'tags')  
    raw_id_fields = ('author',)  #

    ordering = ('-createdAt',)