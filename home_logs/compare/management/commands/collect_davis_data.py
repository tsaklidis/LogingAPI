# coding: utf-8
from django.core.management.base import BaseCommand

from home_logs.compare.scrape import collect

class Command(BaseCommand):
    help = 'Get the data from davis and save to DB. (For use with cron jobs)'

    def handle(self, *args, **options):
        collect()
