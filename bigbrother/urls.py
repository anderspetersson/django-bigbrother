from django.conf import settings
from django.urls import path, re_path
import bigbrother.views

urlpatterns = [
    path('', bigbrother.views.BigBrotherIndexView.as_view(), name='bigbrother_index'),
    re_path('^graph/(?P<slug>[^/]+)/$', bigbrother.views.BigBrotherGraphView.as_view(), name='bigbrother_graph'),
    re_path('^group/(?P<slug>[^/]+)/$', bigbrother.views.BigBrotherGroupView.as_view(), name='bigbrother_group'),
    path('update/', bigbrother.views.BigBrotherUpdateView.as_view(), name='bigbrother_update'),
]
