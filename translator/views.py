from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.

def index(request):
    context = {}
    template = "translator/index.html"
    return render(request, template, context)

