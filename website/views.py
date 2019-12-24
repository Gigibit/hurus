from django.shortcuts import render

def index(request):
    return render(request, 'website/index2.html', {})
