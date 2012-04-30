# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from util.http import wrap_response

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from models import Poem, PoemForm
import datetime
from django.core.cache import cache

def index(request):
    latest_poem_list = Poem.objects.all().order_by('-pub_date')[:10]
    poems = {'latest_poem_list': latest_poem_list}
    template = 'words/index.html'
    return render(request, template, poems)


def queue(request):
    started = int(request.GET.get('started'))
    print "started: " + str(started)
    if started > 0:
        print "Poem has started!"
        q_idx = int(request.GET.get('queue'))
        start_idx = int(request.GET.get('start'))
        bookmark = start_idx + q_idx % 10
        print "where at: " + str(q_idx)
        print "starting point: " + str(start_idx)
    else: 
        bookmark = cache.get('bookmark')
        print "bookmark: " + str(bookmark)  
        
    words = {'bookmark': bookmark, 'words' : cache.get(bookmark)}  
    if words['words'] is None: words = { 'bookmark': -1, 'words' : ['wait', 'wait'] }
    print words
    return wrap_response(words)

def controls(request):
    controls = request.GET
    current = cache.get('controls')
    cache.set('controls', controls)
    print cache.get('controls')
    return wrap_response(current)
    




