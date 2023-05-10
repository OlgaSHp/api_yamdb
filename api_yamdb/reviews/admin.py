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
        'category_id'
    )
    list_editable = ('category_id',)
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
