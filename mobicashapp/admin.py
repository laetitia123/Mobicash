from django.contrib import admin
from django.contrib.auth.models import User
from .models import Project,Profile
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal =('tags',)

# admin.site.register(Editor)
# admin.site.register(Article,ArticleAdmin)
# admin.site.register(tags)
admin.site.register(Project)
admin.site.register(Profile)