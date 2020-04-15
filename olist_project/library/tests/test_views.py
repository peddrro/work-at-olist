from django.test import TestCase
from rest_framework.test import APIClient
from library import models, views

class AuthorViewSetTest(TestCase):
    '''
        TestCase class responsible to test Author endpoint
    '''
    client = APIClient()
    fixtures = ['fake_model_objects.json']

    def test_authors_viewset_availability(self):
        response = self.client.get('/authors/')
        self.assertEquals(response.status_code, 200)
    
    def test_authors_viewset_list(self):
        num_authors = models.Author.objects.count()
        response = self.client.get('/authors/')
        self.assertEquals(response.data.get('count'), num_authors)
    
    def test_authors_viewset_retrieve(self):
        author = models.Author.objects.first()
        response = self.client.get('/authors/1/')
        self.assertEquals(response.data.get('id'), author.pk)