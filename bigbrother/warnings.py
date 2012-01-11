from django.conf import settings
from django.utils.importlib import import_module

class BigBrotherWarning(object):
    unread_warnings = 0

    def send_warning(self, module, warningtype):
        pass

def send_warning(module, warningtype):
    warningmodule, warningname = get_alert_name()
    obj = getattr(warningmodule, warningname)()
    getattr(warningmodule, warningname).send_warning(obj, module=module, warningtype=warningtype)

def get_alert_name():
    warningname = getattr(settings, 'BIGBROTHER_WARNING', None)
    if not warningname:
        warningname = 'bigbrother.warnings.EmailWarning'

    warningmodulename, warningname = warningname.rsplit('.', 1)
    warningmodule = import_module(warningmodulename)
    return warningmodule, warningname

class EmailWarning(BigBrotherWarning):
    def send_warning(self, module=None, warningtype=None):
        from django.core.mail import mail_admins
        subject = 'BigBrother Warning: %s is to %s' % (module.name, warningtype)
        message = 'Warning, the BigBrother module %s have sent an alert because its current value, %s is to %s.'% (module.name, module.get_text(module()), warningtype)
        mail_admins(subject=subject, message=message)

