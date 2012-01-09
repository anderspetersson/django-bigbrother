from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from bigbrother.models import ModuleStat
from bigbrother.core import get_module_list


def index(request):
    
    bb = []

    for m in get_module_list():
        modulename, attr = m.rsplit('.', 1)
        module = import_module(modulename)
        name = getattr(module,attr)().name
        text = getattr(module,attr)().get_text()
        value = getattr(module,attr)().get_val()
        warning = getattr(module,attr)().warning()
        bb.append({'name':name, 'value':value, 'text':text, 'warning':warning})
    
    return render_to_response('bigbrother/index.html', {'bb': bb}, context_instance=RequestContext(request)) 

def graph(request, slug):
    q = ModuleStat.objects.filter(modulename=slug)
    if q.count() >= 7: week = q[q.count()-7:]
    else: week = q
    if q.count() >= 31: month = q[q.count()-31:]
    else: month = q
    if q.count() >= 365: year = q[q.count()-365:]
    else: year = q
    
    if q:
        lastdow = week[week.count()-1].added
        lastdom = month[month.count()-1].added
        lastdoy = year[year.count()-1].added
    return render_to_response('bigbrother/graph.html', locals(), context_instance=RequestContext(request))

def update(request):
    
    bb = []
    
    for m in get_module_list():
        modulename, attr = m.rsplit('.', 1)
        module = import_module(modulename)
        
        if getattr(module,attr)().write_to_db:
            name = getattr(module,attr)().get_slug()
            value = getattr(module,attr)().get_val()
            bb.append({'name':name, 'value':value})
            
    for mo in bb:
        ModuleStat(modulename=mo['name'], value=mo['value']).save()
    
    return HttpResponse(bb)
            

    
