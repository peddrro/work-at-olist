import csv
from django.core.management.base import BaseCommand, CommandError
from library.models import Author

class Command(BaseCommand):
    '''
        Customized command to populate author table from csv file
    '''
    help = "Extracts authors names from csv file and create its objects"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=open)
    
    def handle(self, *args, **options):
        csv_file = options.get('csv_file')
        try:
            reader = csv.DictReader(csv_file)
            new_authors = [Author(name=row.get('name').strip()) for row in reader]
        except Exception as e:
            self.stderr.write(f"Error on text extraction: {str(e)}")
            return
        Author.objects.bulk_create(new_authors, ignore_conflicts=True)
        self.stdout.write("Authors were created")