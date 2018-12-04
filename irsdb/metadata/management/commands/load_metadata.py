import os
import csv
from django.core.management.base import BaseCommand
from metadata.models import *

from django.conf import settings

METADATA_DIRECTORY = settings.METADATA_DIRECTORY
REPORT_COUNT = 100
CANONICAL_VERSION = '2016v3.0'

class Command(BaseCommand):
    help = """
                Erase and reload the metadata tables, one at a time.
            """

    def reload_variables(self, *args, **options):
        print("Deleting variables.")
        Variable.objects.all().delete()
        infile = os.path.join(METADATA_DIRECTORY, "variables.csv")
        infile = open(infile, 'r')
        reader = csv.DictReader(infile)
        for i, row in enumerate(reader):
            if i%REPORT_COUNT == 0:
                print("Created %s rows" % i)

            #if CANONICAL_VERSION in row['versions']:
            #    row['is_canonical'] = True
            #    row['canonical_version'] = CANONICAL_VERSION
            #else:
            #    row['is_canonical'] = False
            Variable.objects.create(**row)
        print("Total Variables %s" % i)

    def reload_groups(self, *args, **options):
        print("Deleting Groups.")
        Group.objects.all().delete()
        infile = os.path.join(METADATA_DIRECTORY, "groups.csv")
        infile = open(infile, 'r')
        reader = csv.DictReader(infile)
        for i, row in enumerate(reader):
            try:
                if row['headless'] == '':
                    row['headless'] = None
            except KeyError:
                pass
            if i%REPORT_COUNT == 0:
                print("Created %s rows" % i)
            Group.objects.create(**row)
        print("Total Groups %s" % i)

    def reload_schedule_parts(self, *args, **options):
        print("Deleting ScheduleParts.")
        SchedulePart.objects.all().delete()
        infile = os.path.join(METADATA_DIRECTORY, "schedule_parts.csv")
        infile = open(infile, 'r')
        reader = csv.DictReader(infile)
        for i, row in enumerate(reader):
            try:
                if row['is_shell'] == '':
                    row['is_shell'] = None
            except KeyError:
                pass
            if i%REPORT_COUNT == 0:
                print("Created %s rows" % i)
            SchedulePart.objects.create(**row)
        print("Total Schedule Parts %s" % i)

    def reload_line_numbers(self, *args, **options):
        print("Deleting LineNumbers.")
        LineNumber.objects.all().delete()
        infile = os.path.join(METADATA_DIRECTORY, "line_numbers.csv")
        infile = open(infile, 'r')
        reader = csv.DictReader(infile)
        for i, row in enumerate(reader):
            if i%REPORT_COUNT == 0:
                print("Created %s rows" % i)
            LineNumber.objects.create(**row)
        print("Total LineNumber created %s" % i)

    def reload_descriptions(self, *args, **options):
        print("Deleting Descriptions.")
        Description.objects.all().delete()
        infile = os.path.join(METADATA_DIRECTORY, "descriptions.csv")
        infile = open(infile, 'r')
        reader = csv.DictReader(infile)
        for i, row in enumerate(reader):
            if i%REPORT_COUNT == 0:
                print("Created %s rows" % i)
            Description.objects.create(**row)
        print("Total Description created %s" % i)

    def handle(self, *args, **options):
        print("Running metadata load on variables.")

        self.reload_variables()
        self.reload_groups()
        self.reload_schedule_parts()
        self.reload_line_numbers()
        self.reload_descriptions()