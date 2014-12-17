#from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
# Create your views here.

from getdbinfo.models import People

def index(response):
    return HttpResponse("Please enter a /getdbinfo/name")

def query_name(response, name):
    person = People.objects.get(first_name=name)
    return JsonResponse(model_to_dict(person))
    #return HttpResponse("name is %s" % person.last_name)