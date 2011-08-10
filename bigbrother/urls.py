from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^$', 'bigbrother.views.index', name='bigbrother_index'),
    url('^update/$', 'bigbrother.views.update', name='bigbrother_update'),
)