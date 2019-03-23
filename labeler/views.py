from django.shortcuts import render
from django.http import HttpResponse

''' Our HTML pages. '''
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')
