import csv
import os
import requests

from django.core.management.base import BaseCommand
from filing.models import Filing
from irsx.settings import WORKING_DIRECTORY

from os.path import isfile, join


class Command(BaseCommand):
    help = '''
    
    '''




    def handle(self, *args, **options):
        infile = open('results.csv', 'r')
        years = {}
        for row in infile:

            try:
                this_year = int(row[0:4])
            except ValueError:
                print("Skipping %s" % row)
                continue

            try:
                years[this_year] += 1
            except KeyError: 
                years[this_year] = 1

        print(years)


