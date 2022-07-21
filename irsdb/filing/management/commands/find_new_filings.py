import csv
import os
import requests

from django.core.management.base import BaseCommand
from filing.models import Filing
from django.conf import settings
from irsx.settings import WORKING_DIRECTORY
from irsx.file_utils import stream_download

from os.path import isfile, join


class Command(BaseCommand):
    help = '''
    Read the yearly csv file line by line and add new lines if
    they don't exist. Lines are added in bulk at the end.
    '''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('year', nargs='+', type=int)

    def get_writer(self, headers):   
        outfilehandle = open('results.csv', 'w')
        dw = csv.DictWriter(outfilehandle, headers, extrasaction='ignore')
        dw.writeheader()
        return dw

    def handle(self, *args, **options):
        print('reviewing findings in %s dir' % WORKING_DIRECTORY)
        headers = ['object_id',] 
        writer = self.get_writer(headers)
        
        onlyfiles = [f for f in os.listdir(WORKING_DIRECTORY) if isfile(join(WORKING_DIRECTORY, f))]
        num_found = 0
        found_files = {}

        for file in onlyfiles:
            
            return_id = file.replace("_public.xml", "")
            
            try:
                this_filing = Filing.objects.get(object_id=return_id)
            except Filing.DoesNotExist:
                print("Filing not present, adding to list")
                found_files['object_id'] = 1
                writer.writerow({'object_id': return_id})

                num_found += 1
        print(found_files)
        print("Found a total of %s filings not entered" % num_found)


                
