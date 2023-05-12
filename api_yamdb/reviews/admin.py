from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    empty_value_display = '-пусто-'
, User

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text',  'author', 'review')



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score')



admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)    


admin.site.register(User, UserAdmin)