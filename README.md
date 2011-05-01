# Django Bigbrother

Django Bigbrother is a modular dashboard app for Django projects.

## Requirements

* Django >= 1.3 (http://pypi.python.org/pypi/django/)

## Installation

		pip install -e git://github.com/anderspetersson/django-bigbrother.git#egg=django-bigbrother
	
## Configuration

1. Add `bigbrother` to your `INSTALLED_APPS`
2. Add modules to `BIGBROTHER_MODULES` in settings.py

		BIGBROTHER_MODULES = (
		    'bigbrother.core.user_count',
		    'bigbrother.core.new_users_today_count',
		    'bigbrother.core.free_disk_space_count',
		)

3. Include `bigbrother.urls` in your top level urls:

		urlpatterns = patterns('', 
			# ...
			url(r'^bigbrother/', include('bigbrother.urls')))