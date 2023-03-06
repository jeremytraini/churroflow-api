import lxml.etree as ET

def invalidate_invoice(invoice, choice, tag_name, text, index):
    '''
    Invalidating the default invoice (AUInvoice.xml) by changing either the tag or the content into a new text.
    Writes the output into a file tests/output.xml

    Arguments:
        invoice (str) - Path to the invoice we want to change
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
        'tests/AUInvoice.xml',
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TEST1',
        1
    )

    invalidate_invoice(
        'tests/AUInvoice.xml',
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoicePeriod', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TEST2',
        1
    )

    invalidate_invoice(
        'tests/InvalidInvoice.xml',
        'content',
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID',
        'Hello World!',
        1
    )

    invalidate_invoice(
        'tests/InvalidInvoice.xml',
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TEST1',
        2
    )
    '''

    tag_counter = 0

    #adding the encoding when the file is opened and written is needed to avoid a charmap error
    with open(invoice, encoding="utf8") as f:
        tree = ET.parse(f)
        root = tree.getroot()

        for elem in root.getiterator():
            try:
                if choice == 'tag' and elem.tag == tag_name:
                    tag_counter += 1
                    if tag_counter == index:
                        elem.tag = text
                elif choice == 'content' and elem.tag == tag_name:
                    elem.text = text
            except AttributeError:
                pass

    # Adding the xml_declaration and method helped keep the header info at the top of the file.
    tree.write('tests/InvalidInvoice.xml', xml_declaration=True, method='xml', encoding="utf8")
