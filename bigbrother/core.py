import datetime
import os
import psutil
from django.template.defaultfilters import slugify

class BigBrotherModule():
    name = 'Unamed'
    write_to_db = True
    prepend_text = ''
    add_text = ''
    
    def get_val(self):
        return None
        
    def get_text(self):
        return '%s%s%s' % (self.prepend_text, self.get_val(), self.add_text)
        
    def get_slug(self):
        return slugify(self.name)

class UserCount(BigBrotherModule):
    name = 'Total Users'
    
    def get_val(self):
        from django.contrib.auth.models import User
        users = User.objects.all()
        return users.count()

        
class NewUsersTodayCount(BigBrotherModule):
    name = 'New Users Today'
    
    def get_val(self):
        from django.contrib.auth.models import User
        curday = datetime.datetime.today()
        users = User.objects.filter(date_joined__year=curday.year, date_joined__month=curday.month, date_joined__day=curday.day)
        return users.count()


class FreeRamCount(BigBrotherModule):
    name = 'Free RAM'
    add_text = ' MB'
    
    def get_val(self):
        return str(psutil.avail_phymem() / (1024 * 1024))


class FreeDiskCount(BigBrotherModule):
    name = 'Free Disk Space'
    add_text = ' GB'
    
    def get_val(self):
        s = os.statvfs('/')
        return str(round((s.f_bavail * s.f_frsize) / ( 1024 * 1024 * 1024.0 ), 1))
