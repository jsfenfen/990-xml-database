from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '''
    remove all filings from a given year by object id. This is faster if indexes are created already.
    '''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('year', nargs=1, type=int)

    def handle(self, *args, **options):
        self.cursor = connection.cursor()
        self.submission_year = int(options['year'][0])

        BASE_QUERY = "(select object_id from filing_filing where submission_year=%s)" % self.submission_year

        all_tables =  connection.introspection.table_names()
        for table in all_tables:
            if table.startswith('return'):  
                query = "delete from %s where object_id in %s" % (table, BASE_QUERY)
                print("Running query: '%s' " % query)
                result = self.cursor.execute(query)
                print("Done '%s'\n" % result )