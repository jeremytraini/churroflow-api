from lxml import etree
from io import StringIO, BytesIO

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

def invalidate_invoice(invoice_text, choice, tag_name, text, index):
    '''
    Invalidating the given invoice by changing either the tag or the content into a new text.
    Changes the index-th tag or content that matches the tag_name.
    Returns the result as a string.

    Arguments:
        invoice_text (str) - The invoice text
        choice (str) - Choice whether the user wants to replace the tag or the content
        tag_name (str) - The tag that we want to change
        text (str) - The replacement text for either the tag or the content 
        index (int) - Which tag to be replaced

    Exceptions:
        None

    Return Value:
        None
    
    Sample Calls:
    invalidate_invoice(
        data,
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TEST1',
        1
    )

    invalidate_invoice(
        data,
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoicePeriod', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TEST2',
        1
    )

    invalidate_invoice(
        data,
        'content',
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID',
        'Hello World!',
        1
    )

    invalidate_invoice(
        data,
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TEST1',
        2
    )
    '''
    
    root = etree.fromstring(invoice_text.encode('utf-8'))

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
        except AttributeError:
            pass

    return etree.tostring(root).decode('utf-8')


def replace_part_of_string(string, start, end, replace):
    return string[:start] + replace + string[end:]

def squeeze_text_inbetween(string, cursor, txt):
    return string[:cursor] + txt + string[cursor:]