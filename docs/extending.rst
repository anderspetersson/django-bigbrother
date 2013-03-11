Extending BigBrother
====================

BigBrother is built to be easy to extend with your custom modules. A Bigbrother-module is subclass of bigbrother.core.BigBrotherModule, Custom modules can live anywhere in your project, to enable them you add the relevant class to the  BIGBROTHER_MODULES setting.

Example Module - NewUsersTodayCount
-----------------------------------

.. code-block:: python
   :linenos:

    class NewUsersTodayCount(BigBrotherModule):
        """
        Module providing a count of new users from django.contrib.auth
        """
        name = 'New Users Today'

        def check_compatible(self):
            from django.conf import settings
            if 'django.contrib.auth' in settings.INSTALLED_APPS:
                return True
            return False

        def get_val(self):
            try:
                from django.contrib.auth import get_user_model
                USER_MODEL = get_user_model()
            except ImportError:
                from django.contrib.auth.models import User as USER_MODEL
            users = USER_MODEL.objects.filter(date_joined=datetime.date.today())
            return users.count()


BigBrotherModule
----------------

.. autoclass:: bigbrother.core.BigBrotherModule
    :members:

Functions
---------

.. autofunction:: bigbrother.core.get_module_list
.. autofunction:: bigbrother.core.get_module_classes
.. autofunction:: bigbrother.core.get_module_by_slug