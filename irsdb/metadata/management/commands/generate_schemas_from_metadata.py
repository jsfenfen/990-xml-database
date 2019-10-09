import os

from django.core.management.base import BaseCommand
from django.conf import settings

from metadata.models import Variable, Group, SchedulePart
from schemas.documentation_utils import most_recent, debracket
from schemas.type_utils import get_django_type, get_sqlalchemy_type

GENERATED_MODELS_DIR = settings.GENERATED_MODELS_DIR
KNOWN_SCHEDULES = settings.KNOWN_SCHEDULES
CANONICAL_VERSION = '2016v3.0'
soft_tab = '    '

class Command(BaseCommand):
    help = """  Generate django model file.
                Hard overwrites the default file.

                SQLAlchemy in development as a CLI option ( -sqlalchemy )
                Pretty rough at this point

            """


    def add_arguments(self, parser):
        parser.add_argument('--sqlalchemy', action='store_true')

        parser.add_argument(
            "--schedule",
            choices=KNOWN_SCHEDULES,
            default=None,
            help='Get only that schedule'
        )

    def write_model_top(self, sked_name, full_name, parent_sked_name, repeating_group_part=None):
        print("Handing part %s %s" % (sked_name, full_name))

        if self.run_django:

            result = "\n#######\n#\n# %s - %s\n" % (parent_sked_name, full_name)
            if repeating_group_part:
                result += "# A repeating structure from %s\n" % (repeating_group_part)
            result += "#\n#######\n"
            ## write the start of the first group:
            result += "\nclass %s(models.Model):\n" % sked_name
            result +=  soft_tab +  "object_id = models.CharField(max_length=31, blank=True, null=True, help_text=\"unique xml return id\")\n"
            result +=  soft_tab +  "ein = models.CharField(max_length=15, blank=True, null=True, help_text=\"filer EIN\")\n"
            if parent_sked_name=='IRS990ScheduleK':
                # It's not clear what the max length is; Return.xsd is unclear
                result +=  soft_tab +  "documentId = models.TextField(blank=True, null=True, help_text=\"documentID attribute\")"


            return result

        elif self.run_sqlalchemy:

            result = "\n#######\n#\n# %s - %s\n" % (parent_sked_name, full_name)
            if repeating_group_part:
                result += "# A repeating structure from %s\n" % (repeating_group_part)
            result += "#\n#######\n"
            ## write the start of the first group:
            result += "\nclass %s(Base):\n%s__tablename__='%s'\n" % (sked_name,soft_tab, sked_name)
            result +=  soft_tab +  "object_id = Column(String(31))\n"
            result +=  soft_tab +  "ein = Column(String(15))\n"
            if parent_sked_name=='IRS990ScheduleK':
                result +=  soft_tab +  "documentId = Column(String(15))\n"

            result +=  soft_tab +  "id = Column(Integer, primary_key=True)\n" # Add a primary key explicitly

            return result

    def write_top_matter(self):
        if self.run_django:
            self.outfile.write("from django.db import models\n")
        elif self.run_sqlalchemy:
            self.outfile.write("from sqlalchemy import Column, Integer, String, BigInteger, Text, Numeric\n")
            self.outfile.write("from sqlalchemy.ext.declarative import declarative_base\n\n")
            self.outfile.write("Base = declarative_base()\n\n")


    def write_variable(self, variable):
        """
        We fallback to a text field, but we expect the types to be filled in where missing
        """
        print("Write variable name %s type %s" % (variable.db_name, variable.db_type))
        if self.run_django:
            variable_output = get_django_type(variable.irs_type)
            result =  "\n" + soft_tab + "%s = models.%s" % (variable.db_name, variable_output)

        elif self.run_sqlalchemy:
            variable_output = get_sqlalchemy_type(variable.irs_type)
            result =  "\n" + soft_tab + "%s = Column(%s)" % (variable.db_name, variable_output)

        # add newline and documentation regardless of where it's going
        result += "\n" + soft_tab + "#"
        if variable.line_number:
            result += " Line number: %s " % most_recent(debracket(variable.line_number))
        if variable.description:
            result += " Description: %s " % most_recent(debracket(variable.description))
        result += " most recent xpath: %s \n" % variable.xpath

        return result

    def write_sked(self, schedule):
        print("Handling schedule %s" % (schedule))

        
        form_parts = SchedulePart.objects.filter(parent_sked=schedule).order_by('ordering')
        for form_part in form_parts:

            model_top = self.write_model_top(
                form_part.parent_sked_part,
                form_part.part_name,
                schedule
            )

            variables_in_this_part = Variable.objects.filter(
                parent_sked_part=form_part.parent_sked_part,
                version_end__in=['','2016', '2017', '2018'],
            ).exclude(in_a_group=True).order_by('ordering',)
            if variables_in_this_part:
                # only write it if it contains anything
                self.outfile.write(model_top)
                print(model_top)

                for variable in variables_in_this_part:
                    this_var = self.write_variable(variable)
                    print(this_var)
                    self.outfile.write(this_var)

        

        groups_in_this_sked = Group.objects.filter(
            parent_sked=schedule,
            version_end='',
        ).order_by('ordering',)

        for group in groups_in_this_sked:
            name = group.db_name 
            if group.description:
                name += " - " + group.description
            model_top = self.write_model_top(
                group.db_name,
                name,
                schedule,
                repeating_group_part=group.parent_sked_part
            )

            variables_in_this_group = Variable.objects.filter(
                    db_table=group.db_name,
                    version_end__in=['','2016', '2017', '2018'],
                ).order_by('ordering',)

            if variables_in_this_group:
                # only write it if it contains anything
                self.outfile.write(model_top)
                print(model_top)

                for variable in variables_in_this_group:
                    this_var = self.write_variable(variable)
                    print(this_var)
                    self.outfile.write(this_var)


    def handle(self, *args, **options):
        print(options)
        self.run_sqlalchemy = options['sqlalchemy']
        self.run_django = not self.run_sqlalchemy    # Only run one or the other.

        file_output = os.path.join(GENERATED_MODELS_DIR, "django_models_auto.py")
        if self.run_sqlalchemy:
            file_output = os.path.join(GENERATED_MODELS_DIR, "sqlalchemy_models_auto.py")
        self.outfile = open(file_output, 'w')

        self.write_top_matter()
        
        schedulename = options.get('schedule')
        if schedulename:
            print("Handling schedule %s" % schedulename)
            self.write_sked(schedulename)
        else:
            for schedulename in KNOWN_SCHEDULES:
                print("Handling schedule %s" % schedulename)
                self.write_sked(schedulename)

