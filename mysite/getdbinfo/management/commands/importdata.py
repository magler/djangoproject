# $ python -V
# Python 3.4.0
# $ python -c "import django; print(django.get_version())"
# 1.7

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from getdbinfo.models import People
import xml.etree.ElementTree as et
import json

class Difflist(object):
    self.create = []
    self.remove = []
    self.update = []

    def __init__(self, new, old):
        #first we need to remove the records that will not be changing.
        for new_item in new:
            if new_item in old:
                new.remove(old.pop(old.index(new_item)))
        
        #list to update
        for old_item in old:
            found = False
            for new_item in new:
                if new_item['id'] == old_item['id']:
                    found = True
                    self.update.append(new_item)
                    new.remove(new_item)
                    old.remove(old_item)
    
        self.remove = old
        self.create = new

class Command(BaseCommand):
    args = 'none required'
    help = 'Imports the people data'
    
    def handle(self, *args, **options):
        new_people_list = []
        data_tree = et.fromstring('<data><person><first_name>Jim</first_name><home/><last_name>Johns</last_name><age>44</age></person><person><first_name>Larry</first_name><home/><last_name>Smith</last_name><age>34</age></person></data>')
        full_list_of_people = People.objects.all()


        for person in data_tree.findall('person'):
            items = {}
            for field in person.iter():
                if not (field.text is None or field.tag == "person"):
                    items[field.tag] = field.text
            new_people_list.append(items)
            
            self.stdout.write(json.dumps(items))
            try:
                people = People.objects.update_or_create(**items)
                people.save()
            except IntegrityError as e:
                #raise CommandError('{} '.format(e))
                self.stdout.write('{}'.format(e))
                pass