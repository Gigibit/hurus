from django.shortcuts import render

def index(request):
    lang = request.LANGUAGE_CODE.upper()
    if lang == 'IT':
        template = 'website/index_it.html'
    elif lang == 'DE':
        template = 'website/index_de.html'
    else : 
        template = 'website/index.html'
    return render(request, template, {})


def privacy(request):
    lang = request.LANGUAGE_CODE.upper()
    if lang == 'IT':
        template = 'website/privacy.html'
    elif lang == 'DE':
        template = 'website/privacy.html'
    else : 
        template = 'website/privacy.html'
    return render(request, template, {})


def terms(request):
    lang = request.LANGUAGE_CODE.upper()
    if lang == 'IT':
        template = 'website/terms.html'
    elif lang == 'DE':
        template = 'website/terms.html'
    else : 
        template = 'website/terms.html'
    return render(request, template, {})