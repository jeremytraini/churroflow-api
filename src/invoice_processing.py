from datetime import datetime
from src.error import InputError, NotFoundError
from src.type_structure import *
from src.database import Invoices, LineItems
from tests.constants import VALID_INVOICE_TEXT
import requests
from src.generation import generate_diagnostic_list

# class LineItems(BaseModel):
#     invoice: ForeignKeyField(Invoices, backref='invoices')
    
#     description: TextField()
#     quantity: IntegerField()
#     unit_price: FloatField()
#     total_price: FloatField()

def get_invoice_field(invoice_data: dict, field: str) -> str:
    if field in invoice_data:
        return invoice_data[field]
    else:
        raise InputError(detail=f"Field {field} not found in invoice")

def store_and_process_invoice(invoice_name: str, invoice_text: str, owner: int) -> int:
    num_errors, num_warnings, _ = generate_diagnostic_list(invoice_text)
    
    if num_errors > 0:
        invoice = Invoices.create(
                name=invoice_name,
                owner=owner,
                date_last_modified=datetime.now(),
                date_added=datetime.now(),
                num_warnings=num_warnings,
                num_errors=num_errors,
                
                is_valid=False,
                text_content=invoice_text,
            )
        return invoice.id
    else:
        response = requests.post(
            "https://macroservices.masterofcubesau.com/api/v3/invoice/render/json",
            headers={
                "accept": "application/json",
                "api-key": "67b158a62fc240d8ba9411c5d4c9e99d",
                'Content-Type': 'multipart/form-data; boundary=------------------------abcdef1234567890'
            },
            data=(
                '--' + '------------------------abcdef1234567890\r\n' +
                'Content-Disposition: form-data; name="file"; filename="invoice.xml"\r\n' +
                'Content-Type: text/xml\r\n\r\n' +
                invoice_text + '\r\n' +
                '--' + '------------------------abcdef1234567890--\r\n'
            )
        )
        
        if response.status_code != 200:
            raise InputError(detail="Could not parse invoice, please check your invoice")
        else:
            invoice_data = response.json()
            supplier_latitude, supplier_longitude = get_lat_long_from_address(invoice_data["AccountingSupplierParty"]["Party"]["PostalAddress"])
            delivery_latitude, delivery_longitude = get_lat_long_from_address(invoice_data["Delivery"]["DeliveryLocation"]["Address"])
            
            print(invoice_data["AccountingSupplierParty"]["Party"]["PartyIdentification"])
            invoice = Invoices.create(
                name=invoice_name,
                owner=owner,
                date_last_modified=datetime.now(),
                date_added=datetime.now(),
                num_warnings=num_warnings,
                num_errors=num_errors,
                
                is_valid=True,
                text_content=invoice_text,
                
                invoice_title=invoice_data["ID"],
                issue_date=invoice_data["IssueDate"],
                due_date=invoice_data["DueDate"],
                
                order_id=invoice_data["OrderReference"]["ID"],
                invoice_start_date=invoice_data["InvoicePeriod"]["StartDate"],
                invoice_end_date=invoice_data["InvoicePeriod"]["EndDate"],
                
                supplier_name=invoice_data["AccountingSupplierParty"]["Party"]["PartyName"]["Name"],
                supplier_abn=int(invoice_data["AccountingSupplierParty"]["Party"]["PartyLegalEntity"]["CompanyID"]["_text"]),
                supplier_latitude=supplier_latitude,
                supplier_longitude=supplier_longitude,
                
                customer_name=invoice_data["AccountingCustomerParty"]["Party"]["PartyName"]["Name"],
                customer_abn=int(invoice_data["AccountingCustomerParty"]["Party"]["PartyLegalEntity"]["CompanyID"]["_text"]),

                delivery_date=invoice_data["Delivery"]["ActualDeliveryDate"],
                delivery_latitude=delivery_latitude,
                delivery_longitude=delivery_longitude,

                customer_contact_name=invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["Name"],
                customer_contact_email=invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["ElectronicMail"],
                customer_contact_phone=invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["Telephone"],
                
                total_amount=   invoice_data["LegalMonetaryTotal"]["PrepaidAmount"]["_text"] +
                                invoice_data["LegalMonetaryTotal"]["PayableAmount"]["_text"],
            )
            return invoice.id

def get_lat_long_from_address(data: str) -> tuple:
    query = []
    
    for field in ["StreetName", "AdditionalStreetName", "CityName", "PostalZone", "CountrySubentity", "AddressLine", "Country"]:
        if field in data:
            if isinstance(data[field], dict):
                query.append(str(list(data[field].values())[0]))
            else:
                query.append(str(data[field]))
    
    response = requests.get(f"https://geocode.maps.co/search", params={
        "q": " ".join(query),
    })
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
    raise InputError(detail="Could not find location of party. Address: " + " ".join(query))

def invoice_processing_upload_text_v2(invoice_name: str, invoice_text: str, owner: int) -> InvoiceID:
    if len(invoice_name) > 100:
        raise InputError(detail="Name cannot be longer than 100 characters")
    
    return InvoiceID(invoice_id=store_and_process_invoice(invoice_name, invoice_text, owner))




