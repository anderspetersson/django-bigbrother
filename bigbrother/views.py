from django.conf import settings
from django.utils.importlib import import_module

from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    
    bb = []

    for m in settings.BIGBROTHER_MODULES:
        modulename, attr = m.rsplit('.', 1)
        module = import_module(modulename)
        name, value = getattr(module,attr)()
        bb.append({'name':name, 'value':value})   
    
    return render_to_response('bigbrother/index.html', {'bb': bb}, context_instance=RequestContext(request))

    
