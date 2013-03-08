from datetime import datetime, timedelta
from django.utils.importlib import import_module
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.db.models import Avg
import qsstats

from bigbrother.models import ModuleStat
from bigbrother.core import get_module_list


class BigBrotherIndexView(TemplateView):
    """
    Produces a overview of installed modules
    """

    template_name = 'bigbrother/index.html'

    def get_overview_data(self):
        data = []
        for m in get_module_list():
            modulename, attr = m.rsplit('.', 1)
            try:
                module = import_module(modulename)
            except ImportError:
                continue
            cls = getattr(module, attr, None)
            if not cls:
                continue
            instance = cls()
            if not instance.check_compatible():
                continue
            data.append({'name': instance.name,
                         'value': instance.get_val(),
                         'text': instance.get_text(),
                         'warning': instance.check_warning(),
                         'link': instance.link_url})
        return data

    def get_context_data(self, **kwargs):
        ctx = super(BigBrotherIndexView, self).get_context_data(**kwargs)
        ctx.update({
            'bb': self.get_overview_data,
        })
        return ctx


class BigBrotherGraphView(TemplateView):
    """
    Shows a individual module and produces the related graph
    """

    template_name = 'bigbrother/graph.html'

    def get_graph_data(self):
        q = ModuleStat.objects.filter(modulename=self.kwargs.get('slug'))
        qs = qsstats.QuerySetStats(q, 'added', Avg('value'))

        week = qs.time_series(datetime.utcnow() - timedelta(weeks=1), datetime.utcnow())
        month = qs.time_series(datetime.utcnow() - timedelta(weeks=4), datetime.utcnow())
        year = qs.time_series(datetime.utcnow() - timedelta(weeks=52), datetime.utcnow(), interval='weeks')

        return {
            'week': week, 'month': month, 'year': year,
            'lastdow': week[-1][0], 'lastdom': month[-1][0], 'lastdoy': year[-1][0],
            'firstdow': week[0][0], 'firstdom': month[0][0], 'firstdoy': year[0][0],
        }

    def get_context_data(self, **kwargs):
        ctx = super(BigBrotherGraphView, self).get_context_data(**kwargs)
        ctx.update(self.get_graph_data())
        return ctx


class BigBrotherUpdateView(View):
    """
    Compatibility view for updating modules
    """
    def get(self, request, *args, **kwargs):
        from .core import update_modules
        update_modules()
        return HttpResponse('ok')
