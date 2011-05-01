from django.contrib.auth.models import User
import datetime
import os
import psutil

def user_count():
    users = User.objects.all()
    return 'Total Users', users.count()
    
def new_users_today_count():
    curday = datetime.datetime.today()
    users = User.objects.filter(date_joined__year=curday.year, date_joined__month=curday.month, date_joined__day=curday.day)
    return 'New Users Today', users.count()

def free_ram_count():
    return 'Free RAM', str(psutil.avail_phymem() / (1024 * 1024))+' MB'

def free_disk_space_count():
    s = os.statvfs('/')
    return 'Free Disk Space', str(round((s.f_bavail * s.f_frsize) / ( 1024 * 1024 * 1024.0 ), 1))+' GB'
    
    