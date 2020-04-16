from django.test import TestCase
from django.core.exceptions import ValidationError
from library import models

class AuthorTestCase(TestCase):
    '''
        TestCase class responsible to test Author model
    '''
    fixtures = ['fake_model_objects.json']

    def setUp(self):
        self.author = models.Author.objects.first()

    def test_author_bad_representation(self):
        self.assertNotEqual(self.author.__str__(), '')
    
    def test_author_good_representation(self):
        self.assertEqual(self.author.__str__(), self.author.name)
    

class BookTestCase(TestCase):
    '''
        TestCase class responsible to test Book model
    '''
    fixtures = ['fake_model_objects.json']

    def setUp(self):
        self.right_book = models.Book.objects.first()
        self.wrong_book = models.Book.objects.last()

    def test_book_bad_representation(self):
        self.assertNotEqual(self.right_book.__str__(), '')
    
    def test_book_good_representation(self):
        self.assertEqual(self.right_book.__str__(), self.right_book.name)
    
    def test_book_ok_year_validation(self):
        self.assertRaises(ValidationError, self.wrong_book.clean)
    
    def test_book_not_ok_year_validation(self):
        self.assertIsNone(self.right_book.clean())
    