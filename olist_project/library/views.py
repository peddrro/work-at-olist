from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from . import models, serializers, filters

class AuthorViewSet(viewsets.ModelViewSet):
    '''
        Manages Author endpoint\n
        The API allows you to retrieve individual authors as well as a list of them
        The API also permits fields filtering
        The API does not allow you to create, update or delete a author
        
    '''
    http_method_names = ['get', 'head']
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = (filters.AuthorFilterSet)
    
class BookViewSet(viewsets.ModelViewSet):
    '''
        Manages Book endpoint\n
        The API allows you to list, retrieve, create, update and delete books
        The API also permits fields filtering
    '''
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = (filters.BookFilterSet)