from django.core.management.base import BaseCommand, CommandError
from getdbinfo.models import People
import xml.etree.ElementTree as et
from pprint import pprint

class Command(BaseCommand):
    args = 'none required'
    help = 'Imports the people data'
    
    def handle(self, *args, **options):
        data_list = et.fromstring('<data><person><first_name>Jim</first_name><last_name>Bobson</last_name><age>66</age></person><person><first_name>Larry</first_name><last_name>Smith</last_name><age>34</age></person></data>')

        for person in data_list.find('person'):
            items = {}
            #for field in person.iter():
            items[person.tag] = person.text
            people = People(**items)
            people.save()
            self.stdout.write('Successfully added person')
            self.stdout.write(pprint(items))