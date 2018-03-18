from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '''
    remove all filings from a given year that appear to be loading errors; where parse_start is true and 
    parse_complete = False.
    '''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('year', nargs=1, type=int)

    def handle(self, *args, **options):
        self.cursor = connection.cursor()
        self.submission_year = int(options['year'][0])

        BASE_QUERY = "(select object_id from filing_filing where parse_started=True and parse_complete=False and submission_year=%s)" % self.submission_year

        all_tables =  connection.introspection.table_names()
        for table in all_tables:
            if table.startswith('return'):  
                query = "delete from %s where object_id in %s" % (table, BASE_QUERY)
                print("Running query: '%s' " % query)
                result = self.cursor.execute(query)
                print("Done '%s'\n" % result )

        cmds = [
            "update filing_filing set parse_started=False where parse_started = True and parse_complete=False and submission_year=%s" % self.submission_year,
            "update filing_filing set parse_complete=False where parse_complete = True and parse_complete=False and submission_year=%s" % self.submission_year,
            "update filing_filing set process_time=Null where parse_started = True and not process_time is Null and parse_complete=False and submission_year=%s" % self.submission_year,
            "update filing_filing set is_error=False where parse_started = True and is_error = True and parse_complete=False and submission_year=%s" % self.submission_year,
            "update filing_filing set key_error_count=Null where parse_started = True and not key_error_count is Null and parse_complete=False and submission_year=%s" % self.submission_year,
            "update filing_filing set error_details =Null where parse_started = True and not error_details is Null and parse_complete=False and submission_year=%s" % self.submission_year]

        for cmd in cmds:
            print("Running query: '%s' " % cmd)
            self.cursor.execute(cmd)
