from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers

class AuthorViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head']
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()
    
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()