from django.shortcuts import render

def index(request):
    lang = request.LANGUAGE_CODE.upper()
    if lang == 'IT':
        template = 'website/index_it.html'
    elif lang == 'DE':
        template = 'website/index_en.html'
    else : 
        template = 'website/index.html'
    print(lang)
    print(lang == 'IT')
    print(template)
    return render(request, template, {})
