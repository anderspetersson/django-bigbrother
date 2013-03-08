import datetime
import os
import psutil
from django.template.defaultfilters import slugify
from django.conf import settings
from bigbrother.warnings import send_warning

def get_module_list():
    default_modules = (
        'bigbrother.core.UserCount',
        'bigbrother.core.NewUsersTodayCount',
        'bigbrother.core.FreeRamCount',
        'bigbrother.core.FreeDiskCount',
    )
    return getattr(settings, 'BIGBROTHER_MODULES', default_modules)

class BigBrotherModule():
    name = 'Unamed Module'
    write_to_db = True
    prepend_text = ''
    add_text = ''
    warning_low = None
    warning_high = None
    link_url = None
    
    def get_val(self):
        raise NotImplementedError('get_val not implemented.')
        
    def get_text(self):
        return '%s%g%s' % (self.prepend_text, self.get_val(), self.add_text)
        
    def get_slug(self):
        return slugify(self.name)

    def check_warning(self):
        if self.warning.high and self.get_val() >= self.warning_high:
            self.warn(warningtype='high')
            return True
        if self.warning.low and self.get_val() <= self.warning_low:
            self.warn(warningtype='low')
            return True
        return False
    
    def warn(self, warningtype):
        send_warning(module=self.__class__, warningtype=warningtype)


class UserCount(BigBrotherModule):
    name = 'Total Users'
    
    def get_val(self):
        try:
            from django.contrib.auth import get_user_model
            USER_MODEL = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User as USER_MODEL
        users = USER_MODEL.objects.all()
        return users.count()

        
class NewUsersTodayCount(BigBrotherModule):
    name = 'New Users Today'
    
    def get_val(self):
        try:
            from django.contrib.auth import get_user_model
            USER_MODEL = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User as USER_MODEL
        curday = datetime.datetime.today()
        users = USER_MODEL.objects.filter(date_joined__year=curday.year, date_joined__month=curday.month, date_joined__day=curday.day)
        return users.count()


class FreeRamCount(BigBrotherModule):
    name = 'Free RAM'
    add_text = ' MB'
    warning_low = 16

    def get_val(self):
        return psutil.phymem_usage()[2] / (1024 * 1024)

class SwapUsage(BigBrotherModule):
    name = 'Swap Usage'
    add_text = ' MB'
    warning_high = 1

    def get_val(self):
        return psutil.virtmem_usage()[1] / (1024 * 1024)

class FreeDiskCount(BigBrotherModule):
    name = 'Free Disk Space'
    add_text = ' GB'
    
    def get_val(self):
        s = os.statvfs('/')
        return round((s.f_bavail * s.f_frsize) / ( 1024 * 1024 * 1024.0 ), 1)
