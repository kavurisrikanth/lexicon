from . import analysis

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# Home view
def home(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        pos_per, pos_tw, neg_per, neg_tw, neu_per, neu_tw, err = analysis.go(search_text)
        
        context = {
            'search_text': search_text,
            'pos_per': pos_per,
            'neg_per': neg_per,
            'neu_per': neu_per,
            'err': err,
        }
    else:
        context = {}

    return render(request, 'learnapp/home.html', context)