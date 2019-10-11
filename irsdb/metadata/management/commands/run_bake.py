import os

from django.core.management.base import BaseCommand
from metadata.models import *

from django.conf import settings

import requests

METADATA_DIRECTORY = settings.METADATA_DIRECTORY
REPORT_COUNT = 100


FILE_SYSTEM_BASE = settings.FILE_SYSTEM_BASE


class Command(BaseCommand):
    help = """
                Bake the site out to files. 
            """

    def hit_url(self, url):
        print("Baking out url %s" % url)
        requests.get(url)

    def run_parts(self):
        all_parts = SchedulePart.objects.all()
        for part in all_parts:
            url = "http://localhost:8000/metadata/parts/" + part.parent_sked_part + ".html"
            self.hit_url(url)

    def run_groups(self):
        all_groups = Group.objects.all()
        for group in all_groups:
            url = "http://localhost:8000/metadata/groups/" + group.db_name + ".html"
            self.hit_url(url)

    def run_variables(self):
        #re_path(r'variable/(?P<db_name>[\w\d\_]+)\-(?P<variable_name>[\w\d]+).html$', views.show_variable),
        all_variables = Variable.objects.all()
        for var in all_variables:
            var_url = "http://localhost:8000/metadata/variable/" + var.db_table + "-" + var.db_name + ".html"
            self.hit_url(var_url)
            xpath_url = "http://localhost:8000/metadata/xpath/"+ var.xpath.replace("/","-") + ".html"
            self.hit_url(xpath_url)


    def run_xpaths(self):
        all_xpaths = Variable.objects.all()
        for xpath in all_xpaths:
            print(xpath)
            #url = "http://localhost:8000/metadata/variable/" + var.db_table + "-" + var.db_name + ".html"
            #self.hit_url(url)

    def run_nav(self):
        self.hit_url("http://localhost:8000/metadata/about.html")
        self.hit_url("http://localhost:8000/metadata/forms.html")

    def create_dirs(self):
        for subdir in ["parts", "groups", "variable", "xpath"]:
            try:
                os.makedirs(os.path.join( FILE_SYSTEM_BASE, "metadata", subdir))
            except FileExistsError:
                print("File %s exists skipping" % subdir)

    def handle(self, *args, **options):
        print("Baking out urls")
        self.create_dirs()
        self.run_nav()
        self.run_parts()
        self.run_groups()
        self.run_variables()

"""
    re_path(r'xpath/(?P<xpath>.+).html', views.show_xpath),
    re_path(r'variable/(?P<db_name>[\w\d\_]+)\-(?P<variable_name>[\w\d]+).html$', views.show_variable),
"""

