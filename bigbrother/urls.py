from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^$', 'bigbrother.views.index', name='bigbrother_index'),
    url('^graph/(?P<slug>[^/]+)/$', 'bigbrother.views.graph', name='bigbrother_graph'),
    url('^update/$', 'bigbrother.views.update', name='bigbrother_update'),
)