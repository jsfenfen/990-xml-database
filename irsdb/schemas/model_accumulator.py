from django.apps import apps
from django.forms import model_to_dict

# Setting too big will create memory problems
BATCH_SIZE = 100
VERBOSE = False

# TODO: allow appname to be passed as an argument. 
APPNAME = 'return'

listtype = type([])

class Accumulator(object):

    def __init__(self):
        self.model_dict = {}
        self.model_cache = {}
        # Expected: 
        # self.model_dict{model_name: [modeldictionary1, modeldictionary2,]...}

    def _clean_restricted(self, dict):
        """ RESTRICTED is only sked b, SSN's appear in a variety of places
            we could do a better job of restricting this
        """ 
        for key in dict.keys():
            if type(dict[key])==listtype:
                print("\n\n***list found %s" % (key))


            # IRS will replace anything they think is a SSN with "XXX-XX-XXXX"
            # this seems to include 9 digit numbers. 
            # The result is that the irs can lengthen fields (breaking max_length)
            # by doing this, so use a formulation that's shorter than this.
            if dict[key]:
                dict[key]=dict[key].replace('XXX-XX-XXXX', '-SSN-')  

                if dict[key]=='RESTRICTED':
                    # These are numeric fields, don't try to save 'RESTRICTED'
                    dict[key]=0


    def _get_model(self, model_name, appname='return'):
        # cache locally so django doesn't try to hit the db every time
        try:
            return self.model_cache[appname + model_name]
        except KeyError:
            self.model_cache[model_name] = apps.get_model(appname, model_name)
            return self.model_cache[model_name]

    def commit_by_key(self, model_name):
        if self.model_dict[model_name]:
            this_model = self._get_model(model_name)
            if (VERBOSE):
                print("Committing %s objects for key %s" % (
                    len(self.model_dict[model_name]),
                    model_name
                    )
                )
            this_model.objects.bulk_create(self.model_dict[model_name])

            # set array to empty
            self.model_dict[model_name] = []

    def add_model(self, model_name, model_dict):
        # An artifact upstream is creating empty rows, with no name and only an ein and object_id
        # This is probably related to the 'empty head' rows in variables.csv, which will be excised by loading this db and analyzing
        if not model_name:
            print("###Model name is missing in object_id %s\ndict=%s!!!" % (model_dict['object_id'], model_dict))
            return
        this_model = self._get_model(model_name)
        self._clean_restricted(model_dict)
        model_instance = this_model(**model_dict)
        try:
            self.model_dict[model_name].append(model_instance)

        except KeyError:
            self.model_dict[model_name]= [model_instance]

        if len(self.model_dict[model_name]) >= BATCH_SIZE:
            self.commit_by_key(model_name)

    def commit_all(self):
        # commit everything
        if (VERBOSE):   
            print("Running commit all! ")
            print(self.object_report())
        for thiskey in self.model_dict.keys():
            if (VERBOSE): 
                print("Commit key %s" % thiskey)
            self.commit_by_key(thiskey)

    def count(self, model_name):
        return len(self.model_dict[model_name])

    def object_report(self):
        total = 0
        for i in self.model_dict.keys():
            thislen = self.count(i)
            total += thislen
            if thislen > 0:
                print("\t%s:%s" % (i, thislen))
        print("Total %s objects" % total)
