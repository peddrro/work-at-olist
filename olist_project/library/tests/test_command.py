from django.test import TestCase
from rest_framework.test import APIClient
from django.core.management import call_command
from io import StringIO
from library import models
import os

class CommandCreateAuthorTest(TestCase):
    '''
        TestCase class responsible to test extract author csv command
    '''

    def test_command_valid_input(self):
        result = StringIO()
        call_command('create_authors', './library/tests/valid_authors.csv', stdout=result)
        self.assertEquals(result.getvalue(), "Authors were created\n")
    
    def test_command_invalid_input(self):
        result = StringIO()
        error = StringIO()
        call_command('create_authors', './library/tests/invalid_authors.csv', stdout=result, stderr=error)
        self.assertNotEquals(result.getvalue(), "Authors were created\n")
        self.assertIn("Error on text extraction", error.getvalue())

    def test_command_populate_author(self):
        old_num_authors = models.Author.objects.count()
        result = StringIO()
        call_command('create_authors', './authors.csv', stdout=result)
        new_num_authors = models.Author.objects.count()
        self.assertGreater(new_num_authors, old_num_authors)