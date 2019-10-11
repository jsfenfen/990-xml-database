from irsx._version import __version__ as irsx_version
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.db import connection
from django.template.loader import render_to_string

from .models import Variable, LineNumber, Description, SchedulePart, Group



KNOWN_SCHEDULES = settings.KNOWN_SCHEDULES


# We're too low rent to install django-bakery
# in the future we should use CBV's and use it
# This app is odd in that it tries to only consume 
# published metadata .csvs, hence oddness in the models
# which reflect the files, rather than the data

# The base of the file system
try:
    FILE_SYSTEM_BASE = settings.FILE_SYSTEM_BASE
except ImportError:
    FILE_SYSTEM_BASE = ''
# When set to true will 'cache' a baked version of the page
# To run a full bake, run a 'scrape' of every page that needs update
# Then deploy files
# Any new static files need to be moved into place, this is just a hack

BAKE_OUT = True

def bake(request, template, context, filepath=None):
    path = request.META['PATH_INFO']
    if filepath:
        path = filepath
    full_path = FILE_SYSTEM_BASE + path # should be an os.join process here


    print("Bake with full_path = %s" % full_path)
    with open(full_path, "w") as f:
        f.write(render_to_string(template, context))


def show_xpath(request, xpath):
    """
    Show a single xpath
    """
    raw_xpath = xpath
    xpath = xpath.replace("-","/")

    print("Xpath is '%s'" % xpath)
    this_variable = get_object_or_404(Variable, xpath=xpath)
    line_numbers = LineNumber.objects.filter(xpath=xpath)
    descriptions = Description.objects.filter(xpath=xpath)
    if len(line_numbers)<2:
        line_numbers = None
    if len(descriptions)<2:
        descriptions = None

    context = {
        'this_variable': this_variable, 
        'line_numbers':line_numbers,
        'descriptions':descriptions
    }
    template = 'metadata/xpath.html'

    if BAKE_OUT:
        filepath = "/metadata/xpath/" + raw_xpath + ".html"
        bake(request, template, context, filepath=filepath)

    return render(request, template, context)

def show_about(request):
    context = {
        'version':irsx_version,
        'update':datetime.now(),
    }
    template = 'metadata/about.html'

    if BAKE_OUT:
        bake(request, template, context)
    return render(request, template, context)

def show_variable(request, db_name, variable_name):
    """
    Show a single variable
    """
    print("Variable is '%s'" % variable_name)
    variables = Variable.objects.filter(db_table=db_name, db_name=variable_name)
    this_variable = variables[0]
    xpaths = variables.values_list('xpath', 'version_start', 'version_end')
    result_xpaths = []
    for xpath in xpaths:
        result_xpaths.append({
            'xpath':xpath[0],
            'url':"/metadata/xpath/" + xpath[0].replace("/","-") + ".html",
            'version_start':xpath[1], 
            'version_end':xpath[2], 
            })

    print("xpaths are %s" % result_xpaths)


    this_variable = variables[0]
    context = {
        'this_variable': this_variable,
        'xpaths':result_xpaths 
    }
    template = 'metadata/variable.html'

    if BAKE_OUT:
        filepath = this_variable.get_absolute_url()
        bake(request, template, context)
    return render(request, template, context)

def show_part(request, part):
    this_part = get_object_or_404(SchedulePart, parent_sked_part=part)
    related_groups = Group.objects.filter(parent_sked_part=part)
    groups = []
    group_names = []
    for group in related_groups:
        if group.db_name not in group_names:
            groups.append({
                'db_name':group.db_name,
                'get_absolute_url':group.get_absolute_url()
            })
            group_names.append(group.db_name)

    variables = Variable.objects.filter(parent_sked_part=part, in_a_group=False).exclude(version_end__in=['2013', '2014', '2015']).order_by('line_number', 'ordering')
    context = {
        'this_part': this_part, 
        'variables':variables,
        'related_groups':groups,
    }
    template = 'metadata/part.html'

    if BAKE_OUT:
        bake(request, template, context) 
    return render(request, template, context)

def show_group(request, group):
    this_group = Group.objects.filter(db_name=group)[0]
    variables = Variable.objects.filter(db_table=group).exclude(version_end__in=['2013', '2014', '2015']).order_by('line_number', 'ordering')

    template = 'metadata/group.html'
    context = {
        'this_group': this_group, 
        'variables':variables,
    }

    if BAKE_OUT:
        bake(request, template, context) 
    return render(request, template,context )

def join_groups_to_parts():
    with connection.cursor() as cursor:
        # Sigh.
        RAW_SQL = """
            SELECT DISTINCT
                metadata_group.parent_sked,
                metadata_group.parent_sked_part,
                metadata_group.db_name,
                metadata_schedulepart.ordering
            FROM    
                metadata_group 
            LEFT JOIN 
                metadata_schedulepart 
            ON metadata_group.parent_sked_part = metadata_schedulepart.parent_sked_part 
            AND metadata_group.parent_sked = metadata_schedulepart.parent_sked
            ORDER BY 
                metadata_group.parent_sked, 
                metadata_schedulepart.ordering;
        """
        cursor.execute(RAW_SQL)
        rows = cursor.fetchall()
    result_obj = []
    for row in rows:
        result_obj.append({
            'parent_sked':row[0],
            'parent_sked_part':row[1],
            'group_name':row[2],
            })
    return result_obj
   

def show_forms(request):
    """
    Show all form parts - this is gnarly and should be baked / cached
    """
    parts = SchedulePart.objects.all().order_by('parent_sked','ordering')
    form_hash = {}
    part_hash = {}

    # Sorta laboriously rebuild data structure from metadata.csv files. They weren't designed for this!
    for schedule in KNOWN_SCHEDULES:
        form_hash[schedule] = {'schedule_name':schedule, 'parts':[]}
    for part in parts:
        try:
            form_hash[part.parent_sked]['parts'].append(part)
        except KeyError:
            form_hash[part.parent_sked] = {'schedule_name':part.parent_sked, 'parts':[part]}

    sked_part_hash = {}
    joined_groups = join_groups_to_parts()
    for jg in joined_groups:
        try:
            sked_part_hash[jg['parent_sked_part']]['groups'].append(jg['group_name'])
        except KeyError:
            sked_part_hash[jg['parent_sked_part']] = {'groups':[jg['group_name']]}

    return_array = []
    for fkey in form_hash.keys():
        this_data_obj = {'sked_name':fkey, 'parts':[]}
        for i, part in enumerate(form_hash[fkey]['parts']):
            part_obj = {}
            part_obj['part'] = part
            part_obj['groups'] = []
            part_obj['name'] = part.parent_sked_part
            try: 
                groups = sked_part_hash[part.parent_sked_part]['groups']
                part_obj['groups'] = groups
            except KeyError:
                part_obj['groups'] = ''
            this_data_obj['parts'].append(part_obj)
        return_array.append(this_data_obj)
            
    print(return_array)
    template = 'metadata/forms.html'
    context = {
        'forms':return_array
    }
    if BAKE_OUT:
        bake(request, template, context) 
    return render(request, template, context)