from django.core.management.base import BaseCommand
from bigbrother.core import update_modules


class Command(BaseCommand):
    help = 'Updates all active modules in BigBrother'

    def handle(self, *args, **options):
        update_modules()
        self.stdout.write('All modules updated successfully')