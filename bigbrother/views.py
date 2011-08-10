from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from bigbrother.models import ModuleStat


def index(request):
    
    bb = []

    for m in settings.BIGBROTHER_MODULES:
        modulename, attr = m.rsplit('.', 1)
        module = import_module(modulename)
        name = getattr(module,attr)().name
        value = getattr(module,attr)().get_text()
        bb.append({'name':name, 'value':value})
    
    return render_to_response('bigbrother/index.html', {'bb': bb}, context_instance=RequestContext(request)) 

def graph(request, slug):
    stats = ModuleStat.objects.filter(modulename=slug)[0:30]    
    return render_to_response('bigbrother/graph.html', {'stats': stats}, context_instance=RequestContext(request))

def update(request):
    
    bb = []
    
    for m in settings.BIGBROTHER_MODULES:
        modulename, attr = m.rsplit('.', 1)
        module = import_module(modulename)
        
        if getattr(module,attr)().write_to_db:
            name = getattr(module,attr)().get_slug()
            value = getattr(module,attr)().get_val()
            bb.append({'name':name, 'value':value})
            
    for mo in bb:
        ModuleStat(modulename=mo['name'], value=mo['value']).save()
    
    return HttpResponse(bb)
            

    
