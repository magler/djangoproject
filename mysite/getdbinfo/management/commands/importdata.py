# $ python -V
# Python 3.4.0
# $ python -c "import django; print(django.get_version())"
# 1.7

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from getdbinfo.models import People
import xml.etree.ElementTree as et
import json

class Command(BaseCommand):
    args = 'none required'
    help = 'Imports the people data'
    
    def handle(self, *args, **options):
        data_list = et.fromstring('<data><person><first_name>Jim</first_name><home/><last_name>Johns</last_name><age>66</age></person><person><first_name>Larry</first_name><home/><last_name>Smith</last_name><age>34</age></person></data>')

        for person in data_list.findall('person'):
            items = {}
            for field in person.iter():
                if not (field.text is None or field.tag == "person"):
                    items[field.tag] = field.text
            
            self.stdout.write(json.dumps(items))
            try:
                people = People(**items)
                people.save()
            except IntegrityError as e:
                raise CommandError('("{}", "{}"): {} '.format(people.first_name, people.last_name, e))