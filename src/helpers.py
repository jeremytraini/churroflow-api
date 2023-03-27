from tempfile import NamedTemporaryFile
from src.type_structure import *
from lxml import etree
import re

def create_temp_file(invoice_text: str) -> str:
    tmp = NamedTemporaryFile(mode='w', delete=False)
    tmp.write(invoice_text)
    tmp.close()
    
    return tmp.name

def string_in_range(min_len:int, max_len:int, input_str:str) -> bool:
    '''
    This function checks if a string is within the ranges of min and max length.

    Arguments:
        min_len (int)   - Minimum length of string
        max_len (int)   - Maximum length of string
        input_str (str) - Input string to check length

    Return Value:
        Returns boolean to whether string is within range or not
    '''

    return len(input_str) >= min_len and len(input_str) <= max_len

def fix_xpath(string):
    def repl(match):
        element_name = match.group(1)
        return f'/*[local-name()=\'{element_name}\']['
    
    pattern = r'\/\*:([A-Za-z]+)\['
    return re.sub(pattern, repl, string)

def get_element_from_xpath(xml_text: str, xpath_expression: str) -> etree.Element:
    root = etree.fromstring(xml_text.encode('utf-8'))

    # Evaluate the XPath expression to get the matching element
    try:
        return root.xpath(fix_xpath(xpath_expression))[0]
    except etree.XPathEvalError:
        return None

def get_line_from_xpath(xml_text: str, xpath_expression: str) -> int:
    element = get_element_from_xpath(xml_text, xpath_expression)
    if element is None:
        return 0
        
    return element.sourceline