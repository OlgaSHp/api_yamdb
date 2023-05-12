from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
