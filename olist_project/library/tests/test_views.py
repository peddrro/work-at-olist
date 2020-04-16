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
    
    def test_authors_viewset_object(self):
        author = models.Author.objects.first()
        response = self.client.get('/authors/1/')
        self.assertEquals(response.data.get('id'), author.pk)
    
    def test_authors_viewset_object_not_found(self):
        response = self.client.get('/authors/999/')
        self.assertEquals(response.status_code, 404)
    
    def test_author_viewset_prohibited_post(self):
        new_author = {
            'name': 'Teste'
        }
        response = self.client.post('/authors/', new_author)
        self.assertNotEquals(response.status_code, 200)
    
    def test_author_viewset_prohibited_put(self):
        author = models.Author.objects.first()
        new_name = {'name': 'Teste name'}
        response = self.client.put(f'/authors/{author.pk}', new_name, content_type='application/json')
        self.assertNotEquals(response.status_code, 200)
    
    def test_author_viewset_prohibited_patch(self):
        author = models.Author.objects.first()
        new_name = {'name': 'Teste name'}
        response = self.client.patch(f'/authors/{author.pk}', new_name, content_type='application/json')
        self.assertNotEquals(response.status_code, 200)

    def test_author_viewset_prohibited_delete(self):
        author = models.Author.objects.first()
        response = self.client.delete(f'/authors/{author.pk}')
        self.assertNotEquals(response.status_code, 204)
    
    def test_author_filtering(self):
        author = models.Author.objects.last()
        response = self.client.get(f"/authors/?name={author.name}")
        self.assertEquals(response.data.get('results')[0].get('id'), author.pk)
    
    def test_author_invalid_filtering(self):
        response = self.client.get(f"/authors/?name=asdfsablablablabla")
        self.assertEquals(response.data.get('count'), 0)

class BookViewSetTest(TestCase):
    '''
        TestCase class responsible to test Book endpoint
    '''
    client = APIClient()
    fixtures = ['fake_model_objects.json']

    def test_books_viewset_availability(self):
        response = self.client.get('/books/')
        self.assertEquals(response.status_code, 200)
    
    def test_books_viewset_list(self):
        num_books = models.Book.objects.count()
        response = self.client.get('/books/')
        self.assertEquals(response.data.get('count'), num_books)
    
    def test_books_viewset_object(self):
        book = models.Book.objects.first()
        response = self.client.get('/books/1/')
        self.assertEquals(response.data.get('id'), book.pk)
    
    def test_books_viewset_object_not_found(self):
        response = self.client.get('/books/999/')
        self.assertEquals(response.status_code, 404)
    
    def test_books_viewset_valid_post(self):
        authors_ids = models.Author.objects.values_list('pk', flat=True)
        new_book = {
            'name': 'Habits', 'edition': 2, 
            'publication_year': 2015, 'authors': authors_ids
        }
        response = self.client.post('/books/', new_book)
        self.assertEquals(response.status_code, 201)
    
    def test_books_viewset_invalid_post(self):
        authors_ids = models.Author.objects.values_list('pk', flat=True)
        new_book = {
            'name': '', 'edition': 2, 
            'publication_year': 2015, 'authors': authors_ids
        }
        response = self.client.post('/books/', new_book)
        self.assertEquals(response.status_code, 400)
    
    def test_books_viewset_valid_partial_update(self):
        book = models.Book.objects.first()
        old_name = book.name
        new_name = {'name': 'Nome teste'}
        self.assertNotEquals(old_name, new_name.get('name'))
        response = self.client.patch(f"/books/{book.pk}/", new_name, content_type='application/json')
        self.assertEquals(response.status_code, 200)
        book = models.Book.objects.first()
        self.assertEquals(book.name, new_name.get('name'))
    
    def test_books_viewset_invalid_partial_update(self):
        book = models.Book.objects.first()
        old_name = book.name
        new_name = {'name': ''}
        self.assertNotEquals(old_name, new_name.get('name'))
        response = self.client.patch(f"/books/{book.pk}/", new_name, content_type='application/json')
        self.assertEquals(response.status_code, 400)
    
    def test_books_viewset_valid_update(self):
        book = models.Book.objects.first()
        modified_book = {'name': 'Nome teste', 'edition': 4, 'publication_year': 2001, 'authors': [2]}
        response = self.client.put(f"/books/{book.pk}/", modified_book, content_type='application/json')
        self.assertEquals(response.status_code, 200)
        book = models.Book.objects.first()
        self.assertEquals(book.name, modified_book.get('name'))

    def test_books_viewset_invalid_update(self):
        book = models.Book.objects.first()
        modified_book = {'name': 'Nome teste', 'publication_year': 2001, 'authors': [2]}
        response = self.client.put(f"/books/{book.pk}/", modified_book, content_type='application/json')
        self.assertEquals(response.status_code, 400)
        book = models.Book.objects.first()
        self.assertNotEquals(book.name, modified_book.get('name'))
    
    def test_books_viewset_valid_delete(self):
        book = models.Book.objects.first()
        response = self.client.delete(f"/books/{book.pk}/")
        self.assertEquals(response.status_code, 204)
        exists = models.Book.objects.filter(pk=book.pk).exists()
        self.assertFalse(exists)
    
    def test_books_viewset_invalid_delete(self):
        exists = models.Book.objects.filter(pk=999).exists()
        self.assertFalse(exists)
        response = self.client.delete(f"/books/999/")
        self.assertEquals(response.status_code, 404)
    
    def test_book_filtering(self):
        book = models.Book.objects.last()
        response = self.client.get(f"/books/?name={book.name}")
        self.assertEquals(response.data.get('results')[0].get('id'), book.pk)
    
    def test_book_invalid_filtering(self):
        response = self.client.get(f"/books/?name=blablablablaasdfdf")
        self.assertEquals(response.data.get('count'), 0)

    def test_book_filtering_multiple_authors_ids(self):
        book = models.Book.objects.first()
        num_authors = book.authors.count()
        response = self.client.get(
            f"/books/?authors={book.authors.first().pk}&authors={book.authors.last().pk}")
        self.assertEquals(response.data.get('results')[0].get('id'), book.authors.first().pk)
        self.assertEquals(response.data.get('results')[1].get('id'), book.authors.last().pk)

    