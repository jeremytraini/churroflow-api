from src.type_structure import *
from src.database import Reports, DoesNotExist
import requests
from src.generation import generate_report


def invoice_upload_text_v1(invoice_name: str, invoice_text: str):
    '''
    This function uploads the inputted text as an invoice into the system

    Arguments:
        invoice_name(string) - Name of the invoice - will be displayed at the top
        invoice_text(string) - Text that will be the content/body of the invoice

    Return Value:
        Returns report_id(integer) - unique identifier with the invoice name and text

    '''
    return {
        "report_id": generate_report(invoice_name, invoice_text)
    }


def invoice_upload_url_v1(invoice_name: str, invoice_url: str):
    '''
    This function uploads a url as an invoice into the system

    Arguments:
        invoice_name(string) - Name of the invoice - will be displayed at the top
        invoice_url(string) - URL contents will be the content/body of the invoice

    Exceptions:
        InvalidURL          - Occurs when an invoice cannot be retrieved from the url

    Return Value:
        Returns report_id(integer) - unique identifier with the invoice name and url details
        
    '''
    response = requests.get(invoice_url)
    if response.status_code != 200:
        raise Exception("Could not retrieve invoice from url")
    
    invoice_text = response.text

    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }


def invoice_upload_file_v1(invoice_name: str, invoice_text: str):
    '''
    This function uploads a url as an invoice into the system

    Arguments:
        invoice_name(string) - Name of the invoice - will be displayed at the top
        invoice_text(string) - Contents of an uploaded file from your device/system

    Return Value:
        Returns report_id(integer) - unique identifier with the invoice name and file details
        
    '''
    return {
        "report_id": generate_report(invoice_name, invoice_text)
    }

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    '''
    This function checks if the given report id is valid and can be located in the database

    Arguments:
        report_id(integer)- unique identifier with the invoice name and url details

    Return Value:
        Returns CheckValidReturn(boolean) - Outputs true or false based on if report_id is found
        
    '''
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    return CheckValidReturn(is_valid=report.is_valid)

def invoice_generate_hash_v1(invoice: TextInvoice) -> str:
    '''
    This function generates a hash based on the given invoice. 

    Arguments:
        invoice(TextInvoice)- Invoice name and contents in the type of TextInvoice

    Return Value:
        Returns HashString - returns a string which uniquely identifies the invoice
        
    '''
    return {}

def invoice_upload_bulk_text_v1(invoices: List[TextInvoice]) -> ReportIDs:
    '''
    This function uploads the inputted text as an invoice into the system

    Arguments:
        invoices(List[TextInvoice]) - Name and contents of multiple invoices from the list of Text 

    Return Value:
        Returns ReportIDs(integer) - unique identifier with the invoice name and text - for multiple invoices

    '''
    return ReportIDs(report_ids=[generate_report(invoice.name, invoice.text) for invoice in invoices])
