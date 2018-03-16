"""
Hand curated list of types that occur in IRS fillings, and their representations
in django and sqlalchemy. The latter is pretty rough.

Defaults to a text field when definitions are missing.

In general the IRS adapts type definitions to shoehorn in old data,
so using current definitions is usually good enough for older stuff... to a point. 

This list is tied to 2013 forwards, maybe this should be namespaced or linked somehow.

USAmountType allows 15 digit ints, so should probably be mapped to biginteger or dealt with.
"""

# A char field longer than MAX_CHAR_FIELD_SIZE will be a text field. 
# Best setting may be db dependent?
MAX_CHAR_FIELD_SIZE = 200 

# based on 2015/2016 schemas, unclear if pre 2013 stuff will break this.
var_types = {
    'USAmountType':{'type':'Integer', 'length':15},
    'BooleanType':{'type':'Char', 'length':5}, # http://www.datypic.com/sc/xsd/t-xsd_boolean.html, legal values = [0,1,'true', 'false']
    'USAmountNNType':{'type':'Integer', 'length':15},
    'CheckboxType':{'type':'Char', 'length':1}, # legal values = ['X'] 
    'StreetAddressType':{'type':'Char', 'length':35},
    'LineExplanationType':{'type':'Char', 'length':100},
    'IntegerNNType':{'type':'Integer', 'length':15},  # max value is unclear, see xsd:Integer vs xsd:int 
    'BusinessNameLine2Type':{'type':'Char', 'length':75},
    'BusinessNameLine1Type':{'type':'Char', 'length':75},
    'RatioType':{'type':'Decimal', 'totalDigits':6, 'fractionDigits':5},
    'StateType':{'type':'Char', 'length':2}, # need list key to translate back ? 
    'CountryType':{'type':'Char', 'length':2},
    'ShortExplanationType':{'type':'Text', 'length':1000},
    'CityType':{'type':'Char', 'length':22},
    'ZIPCodeType':{'type':'Char', 'length':15}, # "ZIP Code - 5 digits plus optional 4 or 7 digits"
    'PersonNameType':{'type':'Char', 'length':35},
    'ExplanationType':{'type':'Text', 'length':9000},
    'YearType':{'type':'Integer', 'length':4},
    'EINType':{'type':'Char', 'length':9},
    'DateType':{'type':'Char', 'length':31}, # unclear http://www.datypic.com/sc/xsd/s-datatypes.xsd.html
    'ShortDescriptionType':{'type':'Char', 'length':20},
    'CountType':{'type':'Integer', 'length':7}, # max length is 6
    'Count2Type':{'type':'Integer', 'length':7}, # max length is 6
    'PhoneNumberType':{'type':'Char', 'length':10},
    'IRS990PFPartVDistriRatioType':{'type':'Decimal', 'totalDigits':12, 'fractionDigits':6}, # was 9, manual fix
    'LargeRatioType':{'type':'Decimal', 'totalDigits':22, 'fractionDigits':12},
    'DecimalNNType':{'type':'Decimal', 'totalDigits':22, 'fractionDigits':2}, # dunno upper bound
    'EFINType':{'type':'Char', 'length':6}, # Type for Electronic Filing Identification No. - 6 digits
    'PINType':{'type':'Char', 'length':5}, # Type for Practitioner PIN, Self-Select PIN and Third Party Designee PIN
    'EmailAddressType':{'type':'Char', 'length':75},
    'SoftwareVersionType':{'type':'Char', 'length':20},
    'TimeType':{'type':'Char', 'length':15}, #  Should be no more than 9 chars, but... [0-9]{2}:[0-9]{2}:[0-9]{2}
    'CUSIPNumberType':{'type':'Char', 'length':9},
    'SSNType':{'type':'Char', 'length':12}, # should be 9 but needs to fit "XXX-XX-XXXX" which has 11
    'DeviceIdType':{'type':'Char', 'length':40},
    'BusinessNameControlType':{'type':'Char', 'length':7}, # max is 4: ([A-Z0-9\-]|&#x26;){1,4}
    'PersonTitleType':{'type':'Char', 'length':35}, 
    'OriginatorType':{'type':'Char', 'length':15},
    'TimestampType':{'type':'Char', 'length':63}, # not sure
    'ISPType':{'type':'Char', 'length':6}, # Type for Intermediate Service Provider No. - 6 uppercase alphanumeric characters
    'PTINType':{'type':'Char', 'length':9}, # Type for Preparer Personal Identification No. - P followed by 8 digits
    'USAmountNegType':{'type':'Integer', 'length':15},
    'IPv6Type':{'type':'Char', 'length':31}, # 1
    'SoftwareIdType':{'type':'Char', 'length':8}, #The Software ID - 8 digits
    'IPv4Type':{'type':'Char', 'length':31},
    'InCareOfNameType':{'type':'Char', 'length':35},
    'TimezoneType':{'type':'Char', 'length':31}
}

def get_django_type(vartype):

    try:
        thisvar = var_types[vartype]
    except KeyError:
        return "TextField(null=True, blank=True)"

    if (thisvar['type'] =='Integer'): 
        if thisvar['length'] < 10:
            return "IntegerField(null=True, blank=True)" # 32 bit: Values from -2147483648 to 2147483647 
        else:
            return "BigIntegerField(null=True, blank=True)" # 64 bit: from: -9223372036854775808 to 9223372036854775807

    elif (thisvar['type']=='Decimal'):
        return "DecimalField(null=True, blank=True, max_digits=%s, decimal_places=%s)" % (thisvar['totalDigits'], thisvar['fractionDigits'])

    elif (thisvar['type']=='Char'):
        if thisvar['length'] <= MAX_CHAR_FIELD_SIZE: 
            return "CharField(null=True, blank=True, max_length=%s)" % thisvar['length']
        else:
            return "TextField(null=True, blank=True)"

    elif (thisvar['type']=='Text'):
        return "TextField(null=True, blank=True)"

    else:
        print("** No match for %s " % thisvar)
        return "TextField(null=True, blank=True)"

def get_sqlalchemy_type(vartype):

    """ This is really rough, not tested, may change """ 

    try:
        thisvar = var_types[vartype]
    except KeyError:
        return "Text"

    if (thisvar['type'] =='Integer'): 
        if thisvar['length'] < 10: # 64 bit should be forced to BigInteger
            return "Integer" 
        else:
            return "BigInteger" 

    elif (thisvar['type']=='Decimal'):
        return "Numeric(precision=%s)" % (thisvar['totalDigits']) 

    elif (thisvar['type']=='Char'):
        if thisvar['length'] <= MAX_CHAR_FIELD_SIZE: 
            return "String(length=%s)" % thisvar['length']
        else:
            return "Text"

    elif (thisvar['type']=='Text'):
        return "Text"

    else:
        print("** No match for %s " % thisvar)
        return "Text"




    

if __name__ == "__main__":
    for key in var_types.keys():
        print("key %s resolve to '%s' and '%s'" % (key, get_django_type(key), get_sqlalchemy_type(key) ) ) 

