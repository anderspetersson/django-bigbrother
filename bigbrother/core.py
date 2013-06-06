import datetime
from django.utils.importlib import import_module
from django.template.defaultfilters import slugify
from django.conf import settings
from bigbrother.models import ModuleStat
from bigbrother.warnings import send_warning


def get_module_list():
    """
    Returns a list of currently enabled modules.
    """
    default_modules = (
        'bigbrother.core.UserCount',
        'bigbrother.core.NewUsersTodayCount',
        'bigbrother.core.FreeRamCount',
        'bigbrother.core.FreeDiskCount',
    )
    return getattr(settings, 'BIGBROTHER_MODULES', default_modules)

def get_graph_list():
    """
    Returns a list of the default graphs.
    """
    default_graphs = (
        'bigbrother.graphs.LastWeekGraph',
        'bigbrother.graphs.LastMonthGraph',
        'bigbrother.graphs.LastYearGraph',
    )
    return getattr(settings, 'BIGBROTHER_GRAPHS', default_graphs)

def get_module_classes(group=None):
    """
    Returns all the module classes defined in the settings
    """
    clslist = []
    for m in get_module_list():
        modulename, attr = m.rsplit('.', 1)
        try:
            module = import_module(modulename)
        except ImportError:
            continue
        cls = getattr(module, attr, None)
        if not cls:
            continue
        if group:
            if slugify(cls.group) != group:
                continue
        clslist.append(cls)
    return clslist

def get_graph_classes():
    """
    Returns all the graph classes defined in settings.
    """
    clslist = []
    for m in get_graph_list():
        modulename, attr = m.rsplit('.', 1)
        try:
            module = import_module(modulename)
        except ImportError:
            continue
        cls = getattr(module, attr, None)
        if not cls:
            continue
        clslist.append(cls)
    return clslist

def get_module_by_slug(slug):
    """
    Searches for a module by slug
    """
    for cls in get_module_classes():
        if cls().get_slug() == slug:
            return cls


def update_modules(logger=None):
    """
    Process all module updates
    """
    now = datetime.datetime.utcnow()
    for cls in get_module_classes():
        instance = cls()
        if not instance.check_compatible():
            continue
        if instance.write_to_db:
            if logger:
                logger.debug('Saving %s - Value: %.2f' % (instance.name, instance.get_val()))
            try:
                module = ModuleStat.objects.get(
                modulename=instance.get_slug(),
                added__year=now.year,
                added__month=now.month,
                added__day=now.day)
                module.value=instance.get_val()
                module.save()
            except ModuleStat.DoesNotExist:
                ModuleStat.objects.create(modulename=instance.get_slug(), value=instance.get_val())


class BigBrotherModule():
    """
    Base class for all BigBrother modules that implements the basic skeleton required for a module.
    """

    name = 'Unnamed Module'
    write_to_db = True
    prefix_text = None
    suffix_text = None
    warning_low = None
    warning_high = None
    link_url = None
    aggregate_function = None
    graphs = get_graph_list()
    group = None

    def check_compatible(self):
        """
        Checks if this module can operate in the current enviroment. It is suggested that you check dependencies in
        this function.
        """
        return True

    def get_aggregate_function(self):
        """
        Return the Django aggregation function this module uses for the aggregated graph views.
        """
        return self.aggregate_function

    def get_val(self):
        """
        Returns the current value
        """
        raise NotImplementedError('get_val not implemented.')

    def get_prefix_text(self):
        """
        Get the text to prefix the value with, for example $ for monetary values.
        """
        return self.prefix_text or ''

    def get_suffix_text(self):
        """
        Get the suffix for the value, for example "Users" for a user count.
        """
        return self.suffix_text or ''

    def get_text(self):
        """
        Returns the current value as formatted text
        """
        return '%s%g%s' % (self.get_prefix_text(), self.get_val(), self.get_suffix_text())

    def get_slug(self):
        """
        Returns the URL friendly slug for the module
        """
        return slugify(self.name)

    def check_warning(self):
        """
        Check if a warning level has been breached
        """
        if self.warning_high and self.get_val() >= self.warning_high:
            self.warn(warningtype='high')
            return True
        if self.warning_low and self.get_val() <= self.warning_low:
            self.warn(warningtype='low')
            return True
        return False

    def warn(self, warningtype):
        send_warning(module=self.__class__, warningtype=warningtype)


class UserCount(BigBrotherModule):
    """
    Module providing a count of users from django.contrib.auth
    """
    name = 'Total Users'
    group = 'User'

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
        users = USER_MODEL.objects.all()
        return users.count()


class NewUsersTodayCount(BigBrotherModule):
    """
    Module providing a count of new users from django.contrib.auth
    """
    name = 'New Users Today'
    group = 'User'

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


class FreeRamCount(BigBrotherModule):
    name = 'Free RAM'
    suffix_text = ' MB'
    warning_low = 16
    group = 'Server'

    def check_compatible(self):
        try:
            import psutil
        except ImportError:
            return False
        return True

    def get_val(self):
        import psutil
        return psutil.phymem_usage()[2] / (1024 * 1024)


class SwapUsage(BigBrotherModule):
    name = 'Swap Usage'
    suffix_text = ' MB'
    warning_high = 1
    group = 'Server'

    def check_compatible(self):
        try:
            import psutil
        except ImportError:
            return False
        return True

    def get_val(self):
        import psutil
        return psutil.virtmem_usage()[1] / (1024 * 1024)


class FreeDiskCount(BigBrotherModule):
    name = 'Free Disk Space'
    suffix_text = ' GB'
    group = 'Server'

    def check_compatible(self):
        import platform
        if platform.system() == 'Windows':
            return False
        return True

    def get_val(self):
        import os
        s = os.statvfs(os.path.split(os.getcwd())[0])
        return round((s.f_bavail * s.f_frsize) / (1024 * 1024 * 1024.0), 1)
