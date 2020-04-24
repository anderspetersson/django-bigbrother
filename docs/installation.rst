Installation
============

1. pip install django-bigbrother
2. Add `bigbrother` to your `INSTALLED_APPS`
3. Run `python manage.py syncdb`
4. If you have `south` installed, run a migration for the `bigbrother` app.
5. Include `bigbrother.urls` in your top level urls:

.. code-block:: python

		urlpatterns = patterns('',
			# ...
			path('bigbrother/', include('bigbrother.urls')))

6. To update statistics you can either call `update_modules()` in `bigbrother.core` or using the `update_bigbrother` management command.
