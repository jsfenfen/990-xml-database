import csv

from django.core.management.base import BaseCommand

from filing.models import Filing

foundation_manifest = "foundation_manifest.csv"
ein_manifest = "ein_manifest.csv"

output_file = "initial_manifest.csv"

headers = ['ein', 'name', 'tax_period', 'form_type', 'is_most_recent', 'missing'] 



class Command(BaseCommand):
    help = '''
    Read a source csv of eins, and find all filings.
    Record which is most recent report.
    Disregard form 990T.
    '''

    def write_ein_details(self, ein):
        print("\n\nprocessing ein '%s'" % ein)
        filings = Filing.objects.filter(ein=ein).order_by('-tax_period', '-sub_date')
        first = 1
        if filings:
            for filing in filings:
                if filing.return_type == '990T':
                    continue

                this_filing_dict = {
                    'name':filing.taxpayer_name,
                    'form_type': filing.return_type,
                    'ein': filing.ein,
                    'tax_period': filing.tax_period,
                    'is_most_recent':first

                }
                print("'%s' - %s - %s - %s - %s - %s" % (filing.taxpayer_name, filing.return_type, filing.sub_date,  filing.tax_period, filing.return_id, filing.object_id))
                self.dw.writerow(this_filing_dict)
                first = 0
        else:
                this_filing_dict = {
                    'ein': ein,
                    'missing': 1
                }
                self.dw.writerow(this_filing_dict)


    def handle(self, *args, **options):

        outfilehandle = open(output_file, 'w')
        self.dw = csv.DictWriter(outfilehandle, headers, extrasaction='ignore')
        self.dw.writeheader()

        reader = open(foundation_manifest, 'r')
        for row in reader:
            self.write_ein_details(row.strip())

        reader = open(ein_manifest, 'r')
        for row in reader:
            self.write_ein_details(row.strip())

