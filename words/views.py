# Create your views here.
from util.http import wrap_response
from util.prequeued import prequeue

from django.shortcuts import render
from models import Poem
from django.core.cache import cache

import random
import cPickle as pickle
import settings

def index(request):
    latest_poem_list = Poem.objects.all().order_by('-pub_date')[:10]
    poems = {'latest_poem_list': latest_poem_list}
    template = 'words/index.html'
    return render(request, template, poems)


def ventana(request):
    latest_poem_list = Poem.objects.all().order_by('-pub_date')[:10]
    poems = {'latest_poem_list': latest_poem_list}
    template = 'words/ventana.html'
    return render(request, template, poems)

def queue(request):
    # named requests override everything
    name = request.GET.get('name')
    print name

    started = int(request.GET.get('started'))
    # sub-queued are the different modes
    subQ = int(request.GET.get('subQ'))
    preQ = int(request.GET.get('preQ'))
    
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
      
    if words['words'] is None: 
        if name != 'undefined':
            q = settings.STATIC_ROOT + "data/" + name + ".pickle"            
        elif preQ >= 0:
            q = settings.STATIC_ROOT + "data/prequeued_" + str(preQ) + ".pickle"
        elif subQ < 0:
            #num = random.randrange(0, 1, 1)
            num = int(request.GET.get('mode'))
            q = settings.STATIC_ROOT + "data/prequeued_" + str(num) + ".pickle" 
        else:
            q = settings.STATIC_ROOT + "data/subqueued_" + str(subQ) + '.pickle' 
               
        with open(q, 'rb') as c: queued = pickle.load(c)
        words = { 'bookmark': -1, 'words' : queued }
    print words
    return wrap_response(words)

def controls(request):
    controls = request.GET
    current = cache.get('controls')
    cache.set('controls', controls)
    print cache.get('controls')
    return wrap_response(current)


