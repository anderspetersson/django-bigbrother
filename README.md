# Django Bigbrother

Django Bigbrother is a modular dashboard app for Django projects.

## Requirements

* django >= 1.3 (http://pypi.python.org/pypi/django/)
* psutil >= 2.1 (http://code.google.com/p/psutil/)

## Installation

		pip install django-bigbrother
	
## Configuration

1. Add `bigbrother` to your `INSTALLED_APPS`
2. Add modules to `BIGBROTHER_MODULES` in settings.py

		BIGBROTHER_MODULES = (
	    	'bigbrother.core.UserCount',
	    	'bigbrother.core.NewUsersTodayCount',
	    	'bigbrother.core.FreeRamCount',
	    	'bigbrother.core.FreeDiskCount',
		)

3. Include `bigbrother.urls` in your top level urls:

		urlpatterns = patterns('', 
			# ...
			url(r'^bigbrother/', include('bigbrother.urls')))
			
## Extending Bigbrother

Bigbrother is built to be easy to extend with your custom modules. A Bigbrother-module is subclass of bigbrother.core.BigBrotherModule, with a "get_val"-method returning the stat you are monitoring, and the value of it. Custom modules can live anywhere in your app, just put the full path to it in BIGBROTHER_MODULES. 

Example module returning number of total users for your site:
		
```python
from bigbrother.core import BigBrotherModule
class UserCount(BigBrotherModule):
    name = 'Total Users'
    
    def get_val(self):
        from django.contrib.auth.models import User
        users = User.objects.all()
        return users.count()
```
		
More examples can be found in [core.py](https://github.com/anderspetersson/django-bigbrother/blob/master/bigbrother/core.py)

## Tracking data for graphs

New in Bigbrother 0.2.0 is the ability to save data and show graphs. This is still in a very early stage. To save data to the database, goto yoururl.com/bigbrother/update/. Setting up a cronjob to do this at midnight every day is recommended. The graphs does currently only support one data entry per day.

## Screenshot

This is how it looks. (With 2 custom modules).

![Screenshot](http://c544632.r32.cf2.rackcdn.com/bigbrother.png)