import re
import unidecode

BRACKET_RE = re.compile(r'\[.*?\]')

def markupify(string):
    """ replace _ with \_  [ not need for all markup ] """
    return string.replace("_","\_")

def debracket(string):
    """ Eliminate the bracketed var names in doc, line strings """
    result = re.sub(BRACKET_RE, ';', string)
    result = unidecode.unidecode(result)
    return result

def most_recent(semicolon_delimited_string):
    result = semicolon_delimited_string.split(";")[-1]
    return result