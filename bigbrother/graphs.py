from bigbrother.core import get_module_by_slug
from bigbrother.models import ModuleStat
from django.db.models import Avg
from datetime import datetime, timedelta
import qsstats


class Graph():
    stopdate = datetime.utcnow()
    showpoints = False

    def get_graph_data(self, slug, *args, **kwargs):
        module = get_module_by_slug(slug)()
        q = ModuleStat.objects.filter(modulename=slug)
        qs = qsstats.QuerySetStats(q, 'added', module.get_aggregate_function() or Avg('value'))
        data = qs.time_series(self.startdate, self.stopdate, interval=self.interval)
        return data


class LineGraph(Graph):
    type = 'line'
    showpoints = True


class BarGraph(Graph):
    type = 'bar'


class LastWeekGraph(LineGraph):
    name = 'Last Week'
    interval = 'days'
    startdate = datetime.utcnow() - timedelta(days=7)


class LastMonthGraph(LineGraph):
    name = 'Last Month'
    interval = 'days'
    startdate = datetime.utcnow() - timedelta(days=30)


class LastYearGraph(LineGraph):
    name = 'Last Year'
    interval = 'weeks'
    startdate = datetime.utcnow() - timedelta(days=365)
