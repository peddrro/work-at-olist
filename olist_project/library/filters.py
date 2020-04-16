import django_filters
from . import models

class AuthorFilterSet(django_filters.FilterSet):
    '''
        Manages filtering on Author endpoint
    '''
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Author
        fields = ['name',]

class BookFilterSet(django_filters.FilterSet):
    '''
        Manages filtering on Book endpoint
    '''
    name = django_filters.CharFilter(lookup_expr='icontains')
    authors = django_filters.ModelMultipleChoiceFilter(
        field_name='authors__id', to_field_name='id', 
        queryset=models.Author.objects.all()
    )

    class Meta:
        model = models.Book
        fields = ['name', 'edition', 'publication_year', 'authors']