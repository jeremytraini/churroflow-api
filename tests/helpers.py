import lxml.etree as ET

def invalidate_invoice(choice, tag_name, text):
    '''
    Invalidating the default invoice (AUInvoice.xml) by changing either the tag or the content into a new text.
    Writes the output into a file tests/output.xml

    Arguments:
        choice (str) - Choice whether the user wants to replace the tag or the content
        tag_name (str) - The tag that we want to change
        text (str) - The replacement text for either the tag or the content 

    Exceptions:
        None

    Return Value:
        None
    
    Sample Calls:
    invalidate_invoice(
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TEST1'
    )

    invalidate_invoice(
        'tag', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoicePeriod', 
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TEST2'
    )

    invalidate_invoice(
        'content',
        '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID',
        'Hello World!'
    )
    '''

    #adding the encoding when the file is opened and written is needed to avoid a charmap error
    with open('tests/AUInvoice.xml', encoding="utf8") as f:
        tree = ET.parse(f)
        root = tree.getroot()

        for elem in root.getiterator():
            try:
                if choice == 'tag' and elem.tag == tag_name:
                    elem.tag = text
                elif choice == 'content' and elem.tag == tag_name:
                    elem.text = text
            except AttributeError:
                pass

    # Adding the xml_declaration and method helped keep the header info at the top of the file.
    tree.write('tests/InvalidInvoice.xml', xml_declaration=True, method='xml', encoding="utf8")
