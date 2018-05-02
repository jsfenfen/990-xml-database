from django.db import models
from django.conf import settings
import os
import re

from irsx import settings as irsx_settings
XML_DIR = irsx_settings.WORKING_DIRECTORY

VERSION_RE=re.compile(r'returnVersion="(20\d\dv\d\.\d)"')

class Filing(models.Model):

    # This is set from the index file.
    submission_year = models.IntegerField(blank=False, null=False, default=0, help_text="Index file year")

    # Verbatim fields set from the csv file
    return_id = models.CharField(max_length=8, blank=False, null=False, default="", help_text="Return ID")
    filing_type = models.CharField(max_length=5, blank=False, null=False, default="", help_text="Always EFILE")
    ein = models.CharField(max_length=9, blank=False, null=False, default="", help_text="Employer ID number")
    tax_period = models.IntegerField(blank=False, null=False, default=0, help_text="Month filed, YYYYMM")
    sub_date = models.CharField(max_length=22, blank=False, null=False, default="", help_text="Submitted date in "
                                "YYYY-MM-DD format. But submitted to whom?")
    taxpayer_name = models.CharField(max_length=100, blank=False, null=False, default="", help_text="Organization name")
    return_type = models.CharField(max_length=5, blank=False, null=False, default="", help_text="Return type")
    dln = models.CharField(max_length=14, blank=False, null=False, default="", help_text="Document Locator Number")
    object_id = models.CharField(max_length=18, blank=False, null=False, default="", help_text="IRS-assigned unique ID")

    # fields we set after processing
    schema_version = models.TextField(null=True, help_text="schema version as it appears, e.g. 2015v2.1 ") 
    tax_year = models.IntegerField(blank=True, null=True, help_text="The year of the tax period, set this from "
                                   "tax_period")
    
    # Processing notes
    parse_started = models.NullBooleanField(help_text="Set this true when parsing begins")
    parse_complete = models.NullBooleanField(null=True, help_text="Set true when data stored")
    process_time = models.DateTimeField(null=True, help_text="When was parsing complete?")
    is_error = models.NullBooleanField(help_text="Was an error of any type encountered during parsing")
    key_error_count = models.IntegerField(blank=True, null=True, help_text="Number of key errors found")
    error_details = models.TextField(null=True, help_text="Describe error condition")

    def get_aws_URL(self):
        return "https://s3.amazonaws.com/irs-form-990/%s_public.xml" % self.object_id

    def get_local_URL(self):
        return os.path.join(XML_DIR, "%s_public.xml" % self.object_id)

    def set_schema_version(self):
        """
        Sets the schema version by trying to read top of file locally.
        Efficient b/c it doesn't parse xml, just runs regex on files second line.
        Doesn't set if file is missing.
        """
        filepath = self.get_local_URL()
        try:
            infile = open(filepath, "r")
        except FileNotFoundError:
            print("File %s is missing, quitting" % filepath)
            return False
        top = infile.read(1024)
        infile.close()
        returnline = top.split("\n")[1]
        result = VERSION_RE.search(returnline)
        if result:
            if result != self.schema_version:
                self.schema_version = result.group(1)
                self.save()
        else:
            print("No result in object_id: %s returnline:%s" % (self.object_id, returnline))


    class Meta:
        managed = True
        indexes = [
            models.Index(fields=['object_id']),
            ]
