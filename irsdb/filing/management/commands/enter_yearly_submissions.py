import csv
import os
import requests

from django.core.management.base import BaseCommand
from filing.models import Filing
from django.conf import settings
from irsx.settings import INDEX_DIRECTORY
from irsx.file_utils import stream_download

BATCH_SIZE = 10000


class Command(BaseCommand):
    help = '''
    Read the yearly csv file line by line and add new lines if 
    they don't exist. Lines are added in bulk at the end.
    '''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('--download', action='store_true') # force download
        parser.add_argument('--enter', action='store_true') # force it to enter


    def handle(self, *args, **options):
        for year in options['year']:
            irs_file_url = 'https://s3.amazonaws.com/irs-form-990/index_%s.csv' % year
            irs_file_len = 0

            force_download = options['download']
            if not force_download:
                response = requests.head(irs_file_url)
                if response.status_code == 404:
                    print('index_%s.csv is not available for download.' % year)
                    continue
                else:
                    irs_file_len = int(response.headers['Content-Length'])

                local_file_path = os.path.join(INDEX_DIRECTORY, "index_%s.csv" % year)

            # Verify index file has been downloaded.
            if not os.path.isfile(local_file_path) or force_download:
                print('Downloading index_%s.csv...' % year)
                stream_download(irs_file_url, local_file_path)
                print('Done!')

            local_file_len = os.path.getsize(local_file_path)
            if irs_file_len == local_file_len:
                print('File index_%s.csv has not changed since the last download.' % year)
                if not options['enter']:
                    continue
            else:
                print('index_%s.csv has changed. Downloading updated file...' % year)
                stream_download(irs_file_url, local_file_path)
                print('Done!')

            print("Entering xml submissions from %s" % local_file_path)
            fh = open(local_file_path, 'r')
            reader = csv.reader(fh)
            rows_to_enter = []

            # ignore header rows

            # python 2 idiom: headers = reader.next() <--- but this is a django 2 thing, so no python 2.X
            next(reader)
            count = 0
            for line in reader:
                (return_id, filing_type, ein, tax_period, sub_date, taxpayer_name, return_type, dln, object_id) = line

                try:
                    obj = Filing.objects.get(object_id=object_id)
                except Filing.DoesNotExist:
                    new_sub = Filing(
                        return_id=return_id,
                        submission_year=year,
                        filing_type=filing_type,
                        ein=ein,
                        tax_period=tax_period,
                        sub_date=sub_date,
                        taxpayer_name=taxpayer_name,
                        return_type=return_type,
                        dln=dln,
                        object_id=object_id
                    )

                    rows_to_enter.append(new_sub)
                    count += 1

                if count % BATCH_SIZE == 0 and count > 0:
                    print("Committing %s total entered=%s" % (BATCH_SIZE, count))
                    Filing.objects.bulk_create(rows_to_enter)
                    print("commit complete")
                    rows_to_enter = []

            Filing.objects.bulk_create(rows_to_enter)
            print("Added %s new entries." % count)
