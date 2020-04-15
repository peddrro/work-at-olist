from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Author(models.Model):
    '''
        Class that holds authors data
    '''
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    '''
        Class that holds books data
    '''
    name = models.CharField(max_length=100)
    edition = models.PositiveSmallIntegerField()
    publication_year = models.PositiveSmallIntegerField()
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if self.publication_year > timezone.now().year:
            raise ValidationError('Publication can not be greater than current year.')
        super().clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    