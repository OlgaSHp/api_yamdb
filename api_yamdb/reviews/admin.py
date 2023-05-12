from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreAdmin (admin.ModelAdmin):
    list_display = ('name', 'slug')


class TitleAdmin (admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category'
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
