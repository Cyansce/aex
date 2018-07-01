from django.shortcuts import render
from django.http import request, HttpResponse
# Create your views here.

def zone(request):
    return HttpResponse([{"id": 1, "zone": "CNC"}, {"id": 2, "zone": "BTC"}])
