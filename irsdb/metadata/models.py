from django.db import models

# Base for import of metadata csv files
class IRSxBase(models.Model):
    parent_sked = models.CharField(max_length=63, blank=True, null=True, help_text="Schedule name", editable=False) 
    parent_sked_part = models.CharField(max_length=63, blank=True, null=True, help_text="db compliant name; NA for ScheduleParts")
    ordering = models.FloatField(null=True, blank=True, help_text="sort order of parts")
    xpath = models.CharField(max_length=255, blank=True, null=True, help_text="xpath", editable=False)

    class Meta:
        abstract = True

class Variable(IRSxBase):
    in_a_group = models.BooleanField(help_text="is this variable in a group", default=False) 
    db_table = models.CharField(max_length=63, blank=True, null=True, help_text="db table", editable=False)
    db_name = models.CharField(max_length=63, blank=True, null=True, help_text="db name", editable=False)
    irs_type = models.CharField(max_length=63, blank=True, null=True, help_text="IRS Type", editable=False)
    db_type = models.CharField(max_length=63, blank=True, null=True, help_text="db type", editable=False)
    line_number = models.CharField(max_length=255, blank=True, null=True, help_text="IRS line number. Missing in returnheader", editable=False)
    description = models.TextField(help_text="IRS-supplied description, from .xsd. ") 
    versions = models.TextField(help_text="semicolon-delimited  ") 
    is_canonical = models.NullBooleanField(help_text="", default=False) 
    canonical_version = models.CharField(max_length=16, blank=True, null=True, help_text="canonical_version", editable=False)

class Group(IRSxBase):
    db_name = models.CharField(max_length=63, blank=True, null=True, help_text="DB name", editable=False) 
    line_number = models.CharField(max_length=255, blank=True, null=True, help_text="IRS-supplied line numbers. Missing for returnheaders", editable=False) 
    description = models.TextField(help_text="IRS-supplied description, from .xsd. ") 
    headless = models.NullBooleanField(help_text="", default=False) 
    versions = models.TextField(help_text="IRS-supplied description, from .xsd. ") 

class SchedulePart(IRSxBase):
    part_name = models.CharField(max_length=255, blank=True, null=True, help_text="Part Name.", editable=False) 
    xml_root = models.CharField(max_length=255, blank=True, null=True, help_text="xpath", editable=False) #is this not equivalent to xpath? 
    is_shell = models.NullBooleanField(help_text="", default=False) 


# For historic reference to precise line_numbers, descriptions

class LineNumber(models.Model):
    xpath = models.CharField(max_length=255, blank=True, null=True, help_text="xpath", editable=False) #is this not equivalent to xpath? 
    versions = models.TextField(help_text="versions") 
    line_number = models.CharField(max_length=255, blank=True, null=True, help_text="IRS-supplied line numbers. Missing for returnheaders", editable=False) 

class Description(models.Model):
    xpath = models.CharField(max_length=255, blank=True, null=True, help_text="xpath", editable=False) #is this not equivalent to xpath? 
    versions = models.TextField(help_text="versions") 
    description = models.TextField(help_text="description") 
