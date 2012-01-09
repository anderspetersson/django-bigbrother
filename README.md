# Django Bigbrother

Django Bigbrother is a modular dashboard app for Django projects.

## Requirements

* django >= 1.3 (http://pypi.python.org/pypi/django/)
* psutil >= 0.3 (http://code.google.com/p/psutil/)

## Installation

1. pip install django-bigbrother

2. Add `bigbrother` to your `INSTALLED_APPS`

3. Include `bigbrother.urls` in your top level urls:

		urlpatterns = patterns('', 
			# ...
			url(r'^bigbrother/', include('bigbrother.urls')))

4. Recommended, but not needed, is to add a cronjob to poll the update view. django-bigbrother ships with a shellscript to make this easy:

		$ bigbrother_install.sh
		Please enter URL to your project. For example: http://www.yoururl.com
		http://www.mywebsite.com
		Installed cronjob: 59   23  *    *   * wget http://www.mywebsite.com/bigbrother/update/
		
	
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
		
### The BigBrotherModule Class have the following attributes:

`name`: A string representing the name of the module. Defaults to 'Unamed Module'

`write_to_db`: Boolean, set to False if you don't want to save stats from this module to the database. Defaults to True

`prepend_text`: String that's beeing added before the actual value on the Dashboard. Defaults to an empty string.

`add_text`: String that's beeing added after the actual value on the Dashboard. Defaults to an empty string.

`warning_low`: Integer or float. Warn bigbrother if the value is equal or less than this value. Set this to None (the default) to disable.

`warning_high`: Integer or float. Warn bigbrother if the value is equal or higher than this value. Set to None (the default) to disable.

## Tracking data for graphs

New in Bigbrother 0.2.0 is the ability to save data and show graphs. This is still in a very early stage. To save data to the database, goto yoururl.com/bigbrother/update/. Setting up a cronjob to do this at midnight every day is recommended. The graphs does currently only support one data entry per day.

The goal is to add functionality to do this via Selery's perodic tasks, or simular in the future.

## Screenshot

This is how it looks. (With 2 custom modules).

![Screenshot](http://c544632.r32.cf2.rackcdn.com/bigbrother.png)
![Screenshot](http://c544632.r32.cf2.rackcdn.com/bigbrother-graph.png)