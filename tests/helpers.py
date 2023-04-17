from lxml import etree
from io import StringIO, BytesIO
from tests.constants import CAC, CBC
from tests.server_calls import clear_v2, auth_register_v2, auth_login_v2
from pytest import fixture

@fixture(autouse=True)
def clear_database():
    try:
        token = auth_register_v2("test", "churros@admin.com", "abc123")["token"]
        clear_v2(token)
    except KeyError:
        token = auth_login_v2("churros@admin.com", "abc123")["access_token"]
        clear_v2(token)

def remove_part_of_string(string, start, end):
    '''
    Removes a part of a string and returns the new string.

    Arguments:
        string (str) - The string we want to change
        start (int) - The start index of the substring we want to remove
        end (int) - The end index of the substring we want to remove

    Exceptions:
        None

    Return Value:
        The new string with the removed part

    Sample Calls:
    remove_part_of_string(VALID_INVOICE_TEXT, 2061, 2062)
    remove_part_of_string(VALID_INVOICE_TEXT, 3508, 3509)
    '''

    return string[:start] + string[end:]


def insert_into_string(string, start, insert):
    return string[:start] + insert + string[start:]

def replace_part_of_string(string, start, end, replace):
    return string[:start] + replace + string[end:]

def append_to_string(string, txt):
    return string + txt

def invalidate_invoice(invoice_text, choice, tag_name, attrib_name, text, index):
    '''
    Invalidating the given invoice by changing either the tag or the content into a new text.
    Changes the index-th tag or content that matches the tag_name.
    Returns the result as a string.

    Arguments:
        invoice_text (str) - The invoice text
        choice (str) - Choice whether the user wants to replace the tag or the content
        tag_name (str) - The tag that we want to change
        attrib_name(str) - The attribute name that we want to change, only used if the choice is 'attrib'
        text (str) - The replacement text for either the tag or the content
        index (int) - Which tag to be replaced

    Exceptions:
        None

    Return Value:
        None

    Sample Calls:
    invalidate_invoice(data, 'tag', 'cbc:CustomizationID', '', 'cbc:TEST1', 1)

    invalidate_invoice(data, 'tag', 'cac:InvoicePeriod', '', 'cac:TEST2', 1)

    invalidate_invoice(data, 'content', 'cbc:CustomizationID', '', 'Hello World!', 1)

    invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    '''

    tags = tag_name.split(':')
    texts = text.split(':')

    # Get the tag name
    if tags[0] == 'cac':
        tag_name = CAC + tags[1]
    elif tags[0] == 'cbc':
        tag_name = CBC + tags[1]

    # Get the text
    if texts[0] == 'cac':
        text = CAC + texts[1]
    elif texts[0] == 'cbc':
        text = CBC + texts[1]
    else:
        text = texts[0]
    
    root = etree.fromstring(invoice_text.encode('utf-8'), parser=None)

    for elem in root.getiterator():
        try:
            if choice == 'tag' and elem.tag == tag_name:
                index -= 1
                if index == 0:
                    elem.tag = text
            elif choice == 'content' and elem.tag == tag_name:
                index -= 1
                if index == 0:
                    elem.text = text
            elif choice == 'attrib' and elem.tag == tag_name:
                index -= 1
                if index == 0:
                    elem.attrib[attrib_name] = text
        except AttributeError:
            pass

    return etree.tostring(root).decode('utf-8')
