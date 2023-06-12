from django.contrib import admin

# Register your models here.
from news.models import Author, Post, PostCategory, Category, Comment

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Comment)