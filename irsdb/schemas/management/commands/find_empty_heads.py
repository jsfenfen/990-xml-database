import os, csv

from django.core.management.base import BaseCommand
from django.apps import apps

from django.conf import settings

from irsx.settings import METADATA_DIRECTORY

class Command(BaseCommand):
    help = """  Find 'empty heads' with no values at all.
        """

    def get_var_hash(self):
        variablefile = os.path.join(METADATA_DIRECTORY, 'variables.csv')
        variables = []
        with open(variablefile, 'r') as variablefh:
            reader = csv.DictReader(variablefh)
            for row in reader:
                key = row['db_table'] + "_" + row['db_name']
                variables.append({'key':key, 'xpath':row['xpath'], 'row':row})
                #print("\t - %s" % key)
        self.variables = variables

    def find_children(self, key):
        results = []
        for var in self.variables:
            if var['xpath'].startswith(key):
                results.append({'name': var['key'], 'xpath': var['xpath'], 'row':var['row']})
        return results

    def find_match(self, key):
        for var in self.variables:
            if var['xpath'] == key:
                return var
        return None

    def find_empty_heads(self):
        count = 0
        for var in self.variables:
            key = var['xpath'] + "/"
            #print("Finding var %s" % key)
            children = self.find_children(key)
            if len(children) > 2:
                print("\n\nHandling xpath=%s" % var['xpath'])
                print("db_table %s; db_name:%s" % (var['row']['db_table'],var['row']['db_name'] ))
                print("Num children: %s" % (len(children)))
                

                print("select count(*) from return_%s where not \"%s\" is null;" % (var['row']['db_table'],var['row']['db_name']))
                this_model = apps.get_model(app_label='return', model_name=var['row']['db_table'])
                if this_model:  
                    #print ("Got model %s name %s" % (this_model, var['row']['db_table'] ))
                    pass
                else:
                    print("model missing %s" % var['row']['db_table'] )
                    assert False
       
                # now see how many elements there are. 
                fieldname = var['row']['db_name']
                notnullcount = this_model.objects.filter(**{fieldname+'__isnull': False}).count()
                print("Count of this field is %s" % notnullcount)
                if notnullcount == 0:
                    count += 1
                    self.writer.writerow([var['xpath']])

        print("Total suspected empty heads: %s" % count) 


    def handle(self, *args, **options):
        outfile = open("emptyheads.csv", "w")

        self.writer = csv.writer(outfile)
        self.variables = None
        self.get_var_hash()
        self.find_empty_heads()
