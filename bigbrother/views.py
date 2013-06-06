from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView, View
from django.db.models import Avg
from django.conf import settings
import qsstats
from bigbrother.models import ModuleStat
from bigbrother.core import get_module_classes, get_graph_classes


class BigBrotherView(TemplateView):
    """
    If the setting BIGBROTHER_REQUIRE_ADMIN is set to True, checks if the user is staff member.
    """

    def get(self, request, *args, **kwargs):
        if settings.BIGBROTHER_REQUIRE_ADMIN and not request.user.is_staff:
            return HttpResponseForbidden()
        else:
            return super(BigBrotherView, self).get(request, *args, **kwargs)

class BigBrotherIndexView(BigBrotherView):
    """
    Produces a overview of installed modules
    """

    template_name = 'bigbrother/index.html'
    group = None

    def get_group(self):
        """
        Makes it possible to override group for a view.
        """

        return self.group

    def get_overview_data(self):
        data = []
        for cls in get_module_classes(self.get_group()):
            instance = cls()
            if instance.check_compatible():
                data.append({'name': instance.name,
                             'value': instance.get_val(),
                             'text': instance.get_text(),
                             'warning': instance.check_warning(),
                             'link': instance.link_url,
                             'group': self.get_group})
        return data

    def get_context_data(self, **kwargs):
        ctx = super(BigBrotherIndexView, self).get_context_data(**kwargs)
        ctx.update({
            'bb': self.get_overview_data,
        })
        return ctx


class BigBrotherGraphView(BigBrotherView):
    """
    Shows a individual module and produces the related graph
    """

    template_name = 'bigbrother/graph.html'

    def get_graph_data(self):
        data = []
        for cls in get_graph_classes():
            instance = cls()
            dataset = instance.get_graph_data(slug=self.kwargs.get('slug'))
            data.append({'name': instance.name,
                         'data': dataset,
                         'startdate': dataset[0][0],
                         'stopdate': dataset[-1][0],
                         'type': instance.type,
                         'showpoints': instance.showpoints})
        return data

    def get_context_data(self, **kwargs):
        ctx = super(BigBrotherGraphView, self).get_context_data(**kwargs)
        ctx.update({
            'bb': self.get_graph_data,
            'modulename': self.kwargs.get('slug')
        })
        return ctx

class BigBrotherGroupView(BigBrotherIndexView):
    """
    Display overview data for a group.
    """

    template_name = 'bigbrother/group.html'

    def get_group(self):
        return self.kwargs.get('slug')


class BigBrotherUpdateView(View):
    """
    Compatibility view for updating modules
    """
    def get(self, request, *args, **kwargs):
        from .core import update_modules
        update_modules()
        return HttpResponse('ok')
