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
        create = []
        remove = []
        update = []
        new_people_list = []
        old_people_list = list(People.objects.all().values())

        data_tree = et.fromstring('<data><person><unique_number>1</unique_number><first_name>Tom</first_name><home/><last_name>Johns</last_name><age>43</age></person><person><unique_number>4</unique_number><first_name>Mark</first_name><home/><last_name>Fish</last_name><age>99</age></person><person><unique_number>2</unique_number><first_name>Billy</first_name><home/><last_name>Cookie</last_name><age>34</age></person><person><unique_number>3</unique_number><first_name>Willy</first_name><home/><last_name>Smith</last_name><age>34</age></person></data>')

        for person in data_tree.findall('person'):
            items = {}
            for field in person.iter():
                if not (field.text is None or field.tag == "person"):
                    if field.tag == 'unique_number' or field.tag == 'age':
                        items[field.tag] = int(field.text)
                    else:
                        items[field.tag] = field.text
            new_people_list.append(items)
        
        for old_item in old_people_list:
            found = False
            del old_item['id']
            for new_item in new_people_list:
                self.stdout.write('Checking if old is the same as new:\n' + str(old_item) +'\n'+str(new_item))
                if new_item == old_item:
                    found=True
                    self.stdout.write('Match Found:\n' + str(old_item) +'\n'+str(new_item))
                    new_people_list.remove(new_item)
                    
                elif new_item['unique_number'] == old_item['unique_number']:
                    found=True
                    self.stdout.write('To Update: ' + str(new_item))
                    update.append(new_item)
                    new_people_list.remove(new_item)
            if not found:
                remove.append(old_item)
    
        create = new_people_list
        update_and_create=update+create
        
        for item in remove:
            people = People.objects.get(unique_number=item['unique_number']).delete()
            self.stdout.write('Deleting: ' + str(item))
            
        for item in update_and_create:
            try:
                obj, created = People.objects.update_or_create(unique_number=item['unique_number'], defaults=item)
                if created:
                    msg = "Created: "
                else:
                    msg = "Updated: "
                self.stdout.write( msg + str(item) )
            except IntegrityError as e:
                self.stdout.write('{}'.format(e))
                pass
        