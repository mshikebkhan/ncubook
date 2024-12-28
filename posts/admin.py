from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Post._meta.fields]
    readonly_fields.remove('reported')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Comment._meta.fields]
    readonly_fields.remove('reported')