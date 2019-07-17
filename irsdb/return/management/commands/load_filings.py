import csv
import os
import requests

from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from filing.models import Filing
from schemas.model_accumulator import Accumulator
from irsx.settings import INDEX_DIRECTORY
from irsx.file_utils import stream_download
from irsx.xmlrunner import XMLRunner
from irsx.filing import InvalidXMLException

# this is how many we process; there's a separate batch size
# in model accumulator for how many are processed
BATCH_SIZE = 1000

class Command(BaseCommand):
    help = '''
    Enter the filings, one by one.
    Loading is done in bulk, though status on the filings is updated one at a time.
   
    '''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('year', nargs=1, type=int)

    def setup(self):
        # get an XMLRunner -- this is what actually does the parsing
        self.xml_runner = XMLRunner()
        self.accumulator = Accumulator()


    def process_sked(self, sked):
        """ Enter just one schedule """ 
        #self.stdout.write("Processing schedule %s" % sked['schedule_name'])
        for part in sked['schedule_parts'].keys():
            partname = part
            partdata = sked['schedule_parts'][part]
            #self.stdout.write("part %s %s" % (partname, partdata))

            self.accumulator.add_model(partname, partdata)

        for groupname in sked['groups'].keys():
            for groupdata in sked['groups'][groupname]:
                #self.stdout.write("group %s %s" % (groupname, groupdata) )
                self.accumulator.add_model(groupname, groupdata)


    def run_filing(self, filing):
        object_id = filing.object_id

        self.stdout.write("run_filing %s" % object_id)

        # if we get a bad xml file, delete the file and retry once
        try:
            parsed_filing = self.xml_runner.run_filing(object_id)
        except InvalidXMLException as e:
            os.remove(e.filepath)
            parsed_filing = self.xml_runner.run_filing(object_id)

        if not parsed_filing:
            self.stderr.write("Skipping filing %s(filings with pre-2013 filings are skipped)\n row details: %s" % (filing, metadata_row))
            return None
        
        schedule_list = parsed_filing.list_schedules()
        #self.stdout.write("sked list is %s" % schedule_list)

        result = parsed_filing.get_result()
            
        keyerrors = parsed_filing.get_keyerrors()
        schema_version = parsed_filing.get_version()
        ## This could be disabled if we don't care about the schema version
        ## This is one save per loaded row...
        if filing.schema_version != schema_version:
            filing.schema_version = schema_version
            filing.save()
  
        if keyerrors:
            # If we find keyerrors--xpaths that are missing from our spec, note it
            has_keyerrors = len(keyerrors) > 0
            self.stderr.write("keyerror: %s" % keyerrors)
            filing.error_details = str(keyerrors)
            filing.key_error_count = len(keyerrors)
            filing.is_error = has_keyerrors
            filing.save()

        if result:
            for sked in result:
                self.process_sked(sked)
        else:
            self.stderr.write("Filing not parsed %s " % object_id)


    def handle(self, *args, **options):

        year = int(options['year'][0])
        if year not in [2014, 2015, 2016, 2017, 2018, 2019]:
            raise RuntimeError("Illegal year `%s`. Please enter a year between 2014 and 2019" % year)
        
        self.stdout.write("Running filings during year %s" % year)
        self.setup()

        process_count = 0
        while True:
            filings=Filing.objects.filter(submission_year=year).exclude(parse_complete=True)[:100]
            if not filings:
                self.stdout.write("Done")
                break

            object_id_list = [f.object_id for f in filings]

            # record that processing has begun
            Filing.objects.filter(object_id__in=object_id_list).update(parse_started=True)

            for filing in filings:
                #self.stdout.write("Handling id %s" % filing.object_id)
                self.run_filing(filing)
                process_count += 1
                if process_count % 1000 == 0:
                    self.stdout.write("Handled %s filings" % process_count)

            # commit anything that's left
            self.accumulator.commit_all()
            # record that all are complete
            Filing.objects.filter(object_id__in=object_id_list).update(process_time=datetime.now(), parse_complete=True)
            self.stdout.write("Processed a total of %s filings" % process_count)
