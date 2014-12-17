from django.core.management.base import BaseCommand, CommandError
from getdbinfo.models import People
import xml.etree.ElementTree as et
from pprint import pprint

class Command(BaseCommand):
    args = 'none required'
    help = 'Imports the people data'
    
    def handle(self, *args, **options):
        data_list = et.fromstring('<data><person><first_name>Jim</first_name><last_name>Bobson</last_name><age>66</age></person><person><first_name>Larry</first_name><last_name>Smith</last_name><age>34</age></person></data>')

        for person in data_list.findall('person'):
            items = {}
            for field in person.iter():
                if field.tag != 'person':
                    self.stdout.write(field.tag)
                    items[field.tag] = field.text
            
            #self.stdout.write(items)
            people = People(**items)
            people.save()
            self.stdout.write('Successfully added')
