from django.conf import settings
from django.conf.urls import patterns, url
import bigbrother.views

urlpatterns = patterns('',
    url('^$', bigbrother.views.BigBrotherIndexView.as_view(), name='bigbrother_index'),
    url('^graph/(?P<slug>[^/]+)/$', bigbrother.views.BigBrotherGraphView.as_view(), name='bigbrother_graph'),
    url('^group/(?P<slug>[^/]+)/$', bigbrother.views.BigBrotherGroupView.as_view(), name='bigbrother_group'),
    url('^update/$', bigbrother.views.BigBrotherUpdateView.as_view(), name='bigbrother_update'),
)
