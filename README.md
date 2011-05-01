# Django Bigbrother

Django Bigbrother is a modular dashboard app for Django projects.

## Requirements

* django >= 1.3 (http://pypi.python.org/pypi/django/)
* psutil >= 2.1 (http://code.google.com/p/psutil/)

## Installation

		pip install -e git://github.com/anderspetersson/django-bigbrother.git#egg=django-bigbrother
	
## Configuration

1. Add `bigbrother` to your `INSTALLED_APPS`
2. Add modules to `BIGBROTHER_MODULES` in settings.py

		BIGBROTHER_MODULES = (
		    'bigbrother.core.user_count',
		    'bigbrother.core.new_users_today_count',
			'bigbrother.core.free_ram_count',
		    'bigbrother.core.free_disk_space_count',
		)

3. Include `bigbrother.urls` in your top level urls:

		urlpatterns = patterns('', 
			# ...
			url(r'^bigbrother/', include('bigbrother.urls')))
			
## Extending Bigbrother

Bigbrother is built to be easy to extend with your custom modules. A Bigbrother-module is simply a function returning the name of the stat you are monitoring, and the value of it. Custom modules can live anywhere in your app, just put the full path to it in BIGBROTHER_MODULES. 

Example module returning number of total users for your site:
		
```python
from django.contrib.auth.models import User
def user_count():
    users = User.objects.all()
    return 'Total Users', users.count()
```
		
More examples can be found in [core.py](https://github.com/anderspetersson/django-bigbrother/blob/master/bigbrother/core.py)

## Screenshot

This is how it looks. (With 2 custom modules).

![Screenshot](http://c544632.r32.cf2.rackcdn.com/bigbrother.png)