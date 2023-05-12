from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expression='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expression='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expression='icontains'
    )
    year = filters.NumberFilter(
        field_name='year',
        lookup_expression='icontains'
    )

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']
