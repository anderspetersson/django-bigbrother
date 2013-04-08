# Django Bigbrother

Django Bigbrother is a modular dashboard app for Django projects.

## Requirements

* django >= 1.4 (http://pypi.python.org/pypi/django/)
* psutil >= 0.3 (http://code.google.com/p/psutil/)

To note, Django 1.4/1.5 do not support timezone sensitive aggregations, so all graphs will return zero values with `USE_TZ` set to `True`.  This has been [resolved](https://github.com/django/django/pull/715) in Django trunk, which should be in for the next release.

## Installation

1. pip install django-bigbrother

2. Add `bigbrother` to your `INSTALLED_APPS`

3. Run `python manage.py syncdb`

4. Include `bigbrother.urls` in your top level urls:

		urlpatterns = patterns('',
			# ...
			url(r'^bigbrother/', include('bigbrother.urls'))

5. To update statistics you can either call `update_modules()` in `bigbrother.core` or using the `update_bigbrother` management command.

## Configuration

Bigbrother ships with a few modules. If you want to remove a or add a module, use the  `BIGBROTHER_MODULES` setting:

		BIGBROTHER_MODULES = (
			# Default Modules:
	    	'bigbrother.core.UserCount',
	    	'bigbrother.core.NewUsersTodayCount',
	    	'bigbrother.core.FreeRamCount',
	    	'bigbrother.core.FreeDiskCount',

	    	# Modules not enabled by default:
	    	# 'bigbrother.core.SwapUsage',
		)

## Extending Bigbrother

Bigbrother is built to be easy to extend with your custom modules. A Bigbrother-module is subclass of bigbrother.core.BigBrotherModule, with a "get_val"-method returning the stat you are monitoring, and the value of it. Custom modules can live anywhere in your app, just put the full path to it in BIGBROTHER_MODULES.

### Example module returning number of total users for your site:

```python
from bigbrother.core import BigBrotherModule
class UserCount(BigBrotherModule):
    name = 'Total Users'

    def get_val(self):
        from django.contrib.auth.models import User
        users = User.objects.all()
        return users.count()
```

### The BigBrotherModule Class have the following functions/attributes:

`name`: A string representing the name of the module. Defaults to 'Unamed Module'

`check_compatible`: A function returning a boolean indicating that the module's dependencies have been met can so can execute.

`write_to_db`: Boolean, set to False if you don't want to save stats from this module to the database. Defaults to True

`prefix_text`: Text to be prefixed onto the display version of the module's value

`suffix_text`: Text to be suffixed onto the display version of the module's value

`warning_low`: Integer or float. Warn bigbrother if the value is equal or less than this value. Set this to None (the default) to disable.

`warning_high`: Integer or float. Warn bigbrother if the value is equal or higher than this value. Set to None (the default) to disable.

`link_url`: Use this to link directly to an external URL from the dashboard.

`aggregate_function`: The Django ORM aggregation object to be used for aggregating the data for graph data.


## Screenshot

This is how it looks. (With 2 custom modules).

![Screenshot](http://c544632.r32.cf2.rackcdn.com/bigbrother.png)
![Screenshot](http://c544632.r32.cf2.rackcdn.com/bigbrother-graph.png)
