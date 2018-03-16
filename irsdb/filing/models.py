from django.db import models
from django.conf import settings

class Filing(models.Model):

    # This is set from the index file.
    submission_year = models.IntegerField(blank=True, null=True, help_text="Index file year")

    # Verbatim fields set from the csv file
    return_id = models.CharField(max_length=31, blank=True, null=True, help_text="return id")
    filing_type = models.CharField(max_length=31, blank=True, null=True, help_text="probably EFILE")
    ein = models.CharField(blank=False, max_length=31)
    tax_period = models.IntegerField(blank=True, null=True, help_text="month filed, YYYYMM")
    sub_date = models.CharField(max_length=31, blank=True, null=True, help_text="Submitted date in YYYY-MM-DD format. But submitted to whom?")
    taxpayer_name = models.CharField(max_length=255, blank=True, null=True, help_text="Organization name")
    return_type = models.CharField(max_length=7, blank=True, null=True, help_text="Return Type")
    dln = models.CharField(max_length=31, blank=True, null=True, help_text="Download number")
    object_id = models.CharField(max_length=31, blank=True, null=True, help_text="unique id")


    ## fields we set after processing
    schema_version = models.TextField(null=True, help_text="schema version as it appears, e.g. 2015v2.1 ") 
    tax_year = models.IntegerField(blank=True, null=True, help_text="The year of the tax period, set this from tax_period")
    
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

    class Meta:
        managed=True
        indexes = [
            models.Index(fields=['object_id']),
            ]
