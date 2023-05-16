from datetime import datetime, timedelta
from src.error import ForbiddenError, InputError, NotFoundError
from src.type_structure import *
from src.database import Invoices, LineItems
import requests
from src.generation import generate_diagnostic_list
from peewee import DoesNotExist, fn
from collections import defaultdict
import calendar


TOLERANCE = 0.001


def get_invoice_field(invoice_data: dict, field: str) -> str:
    if field in invoice_data:
        return invoice_data[field]
    else:
        raise InputError(detail=f"Field {field} not found in invoice")

def process_and_update_invoice(invoice_text: str, invoice: Invoices):
    num_errors, num_warnings, diagonostics = generate_diagnostic_list(invoice_text)
    
    if num_errors > 0:
        invoice.num_warnings = num_warnings
        invoice.num_errors = num_errors
        invoice.is_valid = False
        invoice.text_content = invoice_text
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
            supplier_latitude, supplier_longitude, _ = get_lat_long_from_address(invoice_data["AccountingSupplierParty"]["Party"]["PostalAddress"])
            delivery_latitude, delivery_longitude, delivery_suburb = get_lat_long_from_address(invoice_data["Delivery"]["DeliveryLocation"]["Address"])
            
            invoice.date_last_modified = datetime.now()
            invoice.num_warnings = num_warnings
            invoice.num_errors = num_errors
            invoice.is_valid = True
            invoice.text_content = invoice_text
            
            invoice.invoice_title = invoice_data["ID"]
            invoice.issue_date = invoice_data["IssueDate"]
            invoice.due_date = invoice_data["DueDate"]
            invoice.order_id = invoice_data["OrderReference"]["ID"]
            invoice.invoice_start_date = invoice_data["InvoicePeriod"]["StartDate"]
            invoice.invoice_end_date = invoice_data["InvoicePeriod"]["EndDate"]
            
            invoice.supplier_name = invoice_data["AccountingSupplierParty"]["Party"]["PartyName"]["Name"]
            invoice.supplier_abn = invoice_data["AccountingSupplierParty"]["Party"]["PartyLegalEntity"]["CompanyID"]["_text"]
            invoice.supplier_latitude = supplier_latitude
            invoice.supplier_longitude = supplier_longitude
            
            invoice.customer_name = invoice_data["AccountingCustomerParty"]["Party"]["PartyName"]["Name"]
            invoice.customer_abn = invoice_data["AccountingCustomerParty"]["Party"]["PartyLegalEntity"]["CompanyID"]["_text"]
            
            invoice.delivery_date = invoice_data["Delivery"]["ActualDeliveryDate"]
            invoice.delivery_latitude = delivery_latitude
            invoice.delivery_longitude = delivery_longitude
            invoice.delivery_suburb = delivery_suburb
            
            invoice.customer_contact_name = invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["Name"]
            invoice.customer_contact_email = invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["ElectronicMail"]
            invoice.customer_contact_phone = invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["Telephone"]
            
            invoice.total_amount =  invoice_data["LegalMonetaryTotal"]["PrepaidAmount"]["_text"] + \
                                    invoice_data["LegalMonetaryTotal"]["PayableAmount"]["_text"]
            
            print(invoice)
            invoice.save()
            LineItems.delete().where(LineItems.invoice == invoice).execute()
            for line_item in invoice_data["InvoiceLine"]:
                LineItems.create(
                    invoice=invoice,
                    description=line_item["Item"]["Description"],
                    quantity=line_item["InvoicedQuantity"]["_text"],
                    unit_price=line_item["Price"]["PriceAmount"]["_text"],
                    total_price=line_item["LineExtensionAmount"]["_text"],
                )
    
    return LintReport(
        num_errors=num_errors,
        num_warnings=num_warnings,
        report=diagonostics
    )

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
            supplier_latitude, supplier_longitude, _ = get_lat_long_from_address(invoice_data["AccountingSupplierParty"]["Party"]["PostalAddress"])
            delivery_latitude, delivery_longitude, delivery_suburb = get_lat_long_from_address(invoice_data["Delivery"]["DeliveryLocation"]["Address"])
            
            print(invoice_data["AccountingSupplierParty"]["Party"]["PostalAddress"])
            print("supplier location", supplier_latitude, supplier_longitude)
            print(invoice_data["Delivery"]["DeliveryLocation"]["Address"])
            print("delivery location", delivery_latitude, delivery_longitude)
            
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
                supplier_abn=invoice_data["AccountingSupplierParty"]["Party"]["PartyLegalEntity"]["CompanyID"]["_text"],
                supplier_latitude=supplier_latitude,
                supplier_longitude=supplier_longitude,
                
                customer_name=invoice_data["AccountingCustomerParty"]["Party"]["PartyName"]["Name"],
                customer_abn=invoice_data["AccountingCustomerParty"]["Party"]["PartyLegalEntity"]["CompanyID"]["_text"],

                delivery_date=invoice_data["Delivery"]["ActualDeliveryDate"],
                delivery_latitude=delivery_latitude,
                delivery_longitude=delivery_longitude,
                delivery_suburb=delivery_suburb,

                customer_contact_name=invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["Name"],
                customer_contact_email=invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["ElectronicMail"],
                customer_contact_phone=invoice_data["AccountingCustomerParty"]["Party"]["Contact"]["Telephone"],
                
                total_amount=   invoice_data["LegalMonetaryTotal"]["PrepaidAmount"]["_text"] +
                                invoice_data["LegalMonetaryTotal"]["PayableAmount"]["_text"],
            )
            
            for line_item in invoice_data["InvoiceLine"]:
                LineItems.create(
                    invoice=invoice,
                    description=line_item["Item"]["Description"],
                    quantity=line_item["InvoicedQuantity"]["_text"],
                    unit_price=line_item["Price"]["PriceAmount"]["_text"],
                    total_price=line_item["LineExtensionAmount"]["_text"],
                )
            
            return invoice.id

def get_lat_long_from_address(data: str) -> tuple:
    query = []
    suburb = None
    
    for field in ["StreetName", "AdditionalStreetName", "CityName", "PostalZone", "CountrySubentity", "AddressLine", "Country"]:
        if field in data:
            if isinstance(data[field], dict):
                query.append(str(list(data[field].values())[0]))
            else:
                query.append(str(data[field]))
                
            if field == "AdditionalStreetName":
                suburb = str(data[field])
    
    if not suburb:
        raise InputError(detail="No suburb found")
    
    response = requests.get(f"https://geocode.maps.co/search", params={
        "q": " ".join(query),
    })
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"], suburb
    raise InputError(detail="Could not find location of party. Address: " + " ".join(query))

def invoice_processing_upload_text_v2(invoice_name: str, invoice_text: str, owner: int) -> InvoiceID:
    if len(invoice_name) > 100:
        raise InputError(detail="Name cannot be longer than 100 characters")
    
    return InvoiceID(invoice_id=store_and_process_invoice(invoice_name, invoice_text, owner))

def invoice_processing_lint_v2(invoice_id: int, owner: int, invoice_text: str = None) -> LintReport:
    try:
        invoice = Invoices.get_by_id(invoice_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Invoice with id {invoice_id} not found")
    
    if invoice.owner != None and invoice.owner != owner:
        raise ForbiddenError("You do not own this invoice")
    
    if invoice_text is None:
        invoice_text = invoice.text_content
    else:
        # Update invoice
        return process_and_update_invoice(invoice=invoice, invoice_text=invoice_text)
    
    num_errors, num_warnings, diagonostics = generate_diagnostic_list(invoice_text)
    return LintReport(
        num_errors=num_errors,
        num_warnings=num_warnings,
        report=diagonostics
    )

def invoice_processing_get_v2(invoice_id: int, owner: int, verbose: bool = False):
    try:
        invoice = Invoices.get_by_id(invoice_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Invoice with id {invoice_id} not found")
    
    if invoice.owner != None and invoice.owner != owner:
        raise ForbiddenError("You do not own this invoice")
    
    return invoice.to_json(verbose=verbose)

def invoice_processing_list_all_v2(owner: int, is_valid: bool = None, verbose: bool = False):
    if is_valid is None:
        invoices = Invoices.select().where(Invoices.owner == owner)
    else:
        invoices = Invoices.select().where(Invoices.owner == owner, Invoices.is_valid == is_valid)
    
    return [invoice.to_json(verbose=verbose) for invoice in invoices]

def invoice_processing_delete_v2(invoice_id: int, owner: int):
    try:
        invoice = Invoices.get_by_id(invoice_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Invoice with id {invoice_id} not found")
    
    if invoice.owner != None and invoice.owner != owner:
        raise ForbiddenError("You do not own this invoice")
    
    # Delete line items
    LineItems.delete().where(LineItems.invoice == invoice).execute()
    
    # Delete invoice
    invoice.delete_instance()
    
    return {}

def coord_distance(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def invoice_processing_query_v2(query: str, from_date: str, to_date: str, owner: int, warehouse_lat: str = None, warehouse_long = None):
    if query == "numActiveCustomers":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        # Query the database for active customers within the date range
        active_customers = Invoices.select().where(
            (Invoices.is_valid == True) &
            (Invoices.invoice_end_date >= from_date) &
            (Invoices.invoice_end_date <= to_date) &
            (Invoices.owner == owner)
        ).distinct(Invoices.customer_name)

        # Count the number of active customers
        num_active_customers = active_customers.count()

        # Define the date range to query for the previous 12 months
        prev_year_to_date = to_date - timedelta(days=365)
        prev_year_from_date = prev_year_to_date - timedelta(days=90)

        # Query the database for active customers within the previous 12 months
        prev_year_active_customers = Invoices.select().where(
            (Invoices.is_valid == True) &
            (Invoices.invoice_end_date >= prev_year_from_date) &
            (Invoices.invoice_end_date <= prev_year_to_date) &
            (Invoices.owner == owner)
        ).distinct(Invoices.customer_name)

        # Count the number of active customers in the previous 12 months
        num_prev_year_active_customers = prev_year_active_customers.count()

        # Calculate the percentage change in active customers from the previous 12 months
        if num_prev_year_active_customers == 0:
            percentage_change = 0
        else:
            percentage_change = ((num_active_customers - num_prev_year_active_customers) / num_prev_year_active_customers) * 100

        return {
            "value": num_active_customers,
            "change": percentage_change,
        }
    
    elif query == "numInvoices":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        # Query the database for invoices within the date range
        invoices = Invoices.select().where(
            (Invoices.is_valid == True) &
            (Invoices.invoice_end_date >= from_date) &
            (Invoices.invoice_end_date <= to_date) &
            (Invoices.owner == owner)
        )

        # Count the number of invoices
        num_invoices = invoices.count()

        # Define the date range to query for the previous 12 months
        prev_year_to_date = to_date - timedelta(days=365)
        prev_year_from_date = prev_year_to_date - timedelta(days=90)

        # Query the database for invoices within the previous 12 months
        prev_year_invoices = Invoices.select().where(
            (Invoices.is_valid == True) &
            (Invoices.is_valid == True) &
            (Invoices.invoice_end_date >= prev_year_from_date) &
            (Invoices.invoice_end_date <= prev_year_to_date) &
            (Invoices.owner == owner)
        )

        # Count the number of invoices in the previous 12 months
        num_prev_year_invoices = prev_year_invoices.count()

        # Calculate the percentage change in invoices from the previous 12 months
        if num_prev_year_invoices == 0:
            percentage_change = 0
        else:
            percentage_change = ((num_invoices - num_prev_year_invoices) / num_prev_year_invoices) * 100

        return {
            "value": num_invoices,
            "change": percentage_change,
        }
    
    elif query == "averageDeliveryTime":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        query = (Invoices.select(fn.avg(Invoices.delivery_date - Invoices.invoice_start_date).alias('avg_delivery_time'))
         .where((Invoices.is_valid == True) &
                (Invoices.invoice_start_date >= from_date) &
                (Invoices.invoice_start_date <= to_date) &
                (Invoices.owner == owner)))

        result = query.scalar()

        # calculate the percentage change from the previous 12 months
        previous_year_end = from_date - timedelta(days=1)
        previous_year_start = previous_year_end - timedelta(days=365)

        previous_year_query = (Invoices.select(fn.avg(Invoices.delivery_date - Invoices.invoice_start_date).alias('avg_delivery_time'))
         .where((Invoices.is_valid == True) &
                (Invoices.invoice_start_date >= previous_year_start) &
                (Invoices.invoice_start_date <= previous_year_end) &
                (Invoices.owner == owner)))

        previous_year_result = previous_year_query.scalar()

        if previous_year_result:
            percentage_change = (result - previous_year_result) / previous_year_result * 100
        else:
            percentage_change = 0

        return {
            "value": result,
            "change": percentage_change
        }
        
    elif query == "avgDeliveryDistance":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        query = (Invoices.select(Invoices.supplier_latitude, Invoices.supplier_longitude, Invoices.delivery_latitude, Invoices.delivery_longitude)
                .where((Invoices.is_valid == True) &
                       (Invoices.invoice_start_date >= from_date) &
                       (Invoices.invoice_start_date <= to_date) &
                       (Invoices.owner == owner)))
        
        total = 0
        number = 0
        for invoice in query:
            total += coord_distance(invoice.supplier_latitude, invoice.supplier_longitude, invoice.delivery_latitude, invoice.delivery_longitude)
            number += 1
        
        if number:
            average = total / number
        else:
            average = 0
        
        # calculate the percentage change from the previous 12 months
        previous_year_end = from_date - timedelta(days=1)
        previous_year_start = previous_year_end - timedelta(days=365)

        previous_year_query = (Invoices.select(Invoices.supplier_latitude, Invoices.supplier_longitude, Invoices.delivery_latitude, Invoices.delivery_longitude)
                .where((Invoices.is_valid == True) &
                       (Invoices.invoice_start_date >= previous_year_start) &
                       (Invoices.invoice_start_date <= previous_year_end) &
                       (Invoices.owner == owner)))

        previous_year_total = 0
        previous_year_number = 0
        for invoice in previous_year_query:
            previous_year_total += coord_distance(invoice.supplier_latitude, invoice.supplier_longitude, invoice.delivery_latitude, invoice.delivery_longitude)
            previous_year_number += 1
        
        if previous_year_number:
            previous_year_average = previous_year_total / previous_year_number
        else:
            previous_year_average = 0
        
        if previous_year_average:
            percentage_change = (average - previous_year_average) / previous_year_average * 100
        else:
            percentage_change = 0
        
        return {
            "value": average,
            "change": percentage_change
        }
        
    elif query == "clientDataTable":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        # Get name, total invoices and total invoice value for each client
        
        query = (Invoices.select(Invoices.customer_name,
                                 fn.COUNT(Invoices.id).alias('total_invoices'),
                                 fn.SUM(Invoices.total_amount).alias('total_invoice_value'))
                    .where((Invoices.is_valid == True) &
                           (Invoices.invoice_start_date >= from_date) &
                           (Invoices.invoice_start_date <= to_date) &
                           (Invoices.owner == owner))
        )
        
        query = query.group_by(Invoices.customer_name)
        
        client_data = []
        for i, invoice in enumerate(query):
            client_data.append({
                "id": i,
                "name": invoice.customer_name,
                "total-deliveries": invoice.total_invoices,
                "total-revenue": '{:.2f}'.format(round(invoice.total_invoice_value, 2))
            })
            
        return {
            "data": client_data
        }
        
    elif query == "suburbDataTable":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        # Get suburb name, total deliveries, total revenue and average delivery time for each suburb
        
        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)
            suburb_query = (Invoices
                    .select(Invoices.delivery_suburb,
                            fn.COUNT('*').alias('total_deliveries'),
                            fn.SUM(Invoices.total_amount).alias('total_revenue'),
                            fn.AVG(Invoices.delivery_date - Invoices.invoice_start_date).alias('avg_delivery_time'))
                    .where((Invoices.is_valid == True) &
                        (Invoices.owner == owner) &
                        (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                        (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                        (Invoices.invoice_start_date >= from_date) &
                        (Invoices.invoice_start_date <= to_date))
                    .group_by(Invoices.delivery_suburb))

            result = {"data": []}

            for i, suburb in enumerate(suburb_query):
                suburb_data = {
                    "id": i,
                    "name": suburb.delivery_suburb if suburb.delivery_suburb else "Not Specified",
                    "total-deliveries": suburb.total_deliveries,
                    "total-revenue": suburb.total_revenue,
                    "avg-delivery-time": suburb.avg_delivery_time
                }
                result["data"].append(suburb_data)
        else:
            suburb_query = (Invoices
                    .select(Invoices.delivery_suburb,
                            fn.COUNT('*').alias('total_deliveries'),
                            fn.SUM(Invoices.total_amount).alias('total_revenue'),
                            fn.AVG(Invoices.delivery_date - Invoices.invoice_start_date).alias('avg_delivery_time'))
                    .where((Invoices.is_valid == True) &
                        (Invoices.owner == owner) &
                        (Invoices.invoice_start_date >= from_date) &
                        (Invoices.invoice_start_date <= to_date))
                    .group_by(Invoices.delivery_suburb))

            result = {"data": []}

            for i, suburb in enumerate(suburb_query):
                suburb_data = {
                    "id": i,
                    "name": suburb.delivery_suburb if suburb.delivery_suburb else "Not Specified",
                    "total-deliveries": suburb.total_deliveries,
                    "total-revenue": suburb.total_revenue,
                    "avg-delivery-time": suburb.avg_delivery_time
                }
                result["data"].append(suburb_data)
        
        return result
    
    elif query == "warehouseProductDataTable":
        # Convert from_date and to_date to datetime objects
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)

            # Query the database and calculate the desired values
            results = []
            line_items = (LineItems.select(LineItems.description,
                                        fn.SUM(LineItems.quantity).alias('total_units'),
                                        fn.SUM(LineItems.total_price).alias('total_value'))
                                .join(Invoices)
                                .where((Invoices.is_valid == True) &
                                        (Invoices.owner == owner) &
                                        (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                                        (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                                        (Invoices.invoice_start_date >= from_date) &
                                        (Invoices.invoice_start_date <= to_date))
                                .group_by(LineItems.description))

            for i, item in enumerate(line_items):
                # Append the result to the list
                result = {
                    "id": i,
                    "name": item.description,
                    "total-units": item.total_units,
                    "total-value": item.total_value,
                }
                results.append(result)
        else:
            # Query the database and calculate the desired values
            results = []
            line_items = (LineItems.select(LineItems.description,
                                        fn.SUM(LineItems.quantity).alias('total_units'),
                                        fn.SUM(LineItems.total_price).alias('total_value'))
                                .join(Invoices)
                                .where((Invoices.is_valid == True) &
                                        (Invoices.owner == owner) &
                                        (Invoices.invoice_start_date >= from_date) &
                                        (Invoices.invoice_start_date <= to_date))
                                .group_by(LineItems.description))

            for i, item in enumerate(line_items):
                # Append the result to the list
                result = {
                    "id": i,
                    "name": item.description,
                    "total-units": item.total_units,
                    "total-value": item.total_value,
                }
                results.append(result)

        # Create the final output dictionary
        return {"data": results}
        
    elif query == "heatmapCoords":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        query = (Invoices.select(Invoices.delivery_latitude, Invoices.delivery_longitude, Invoices.total_amount)
                .where((Invoices.is_valid == True) &
                       (Invoices.invoice_start_date >= from_date) &
                       (Invoices.invoice_start_date <= to_date) &
                       (Invoices.owner == owner)))
        
        delivery_coords = []
        for invoice in query:
            delivery_coords.append({
                "lat": invoice.delivery_latitude,
                "lng": invoice.delivery_longitude,
                "count": invoice.total_amount
                })
        
        return {
            "data": delivery_coords
        }
    
    elif query == "warehouseCoords":
        warehouse_coords = []
        query = (Invoices.select(Invoices.supplier_latitude, Invoices.supplier_longitude, Invoices.supplier_name, Invoices.total_amount)
            .where((Invoices.is_valid == True) &
                   (Invoices.owner == owner))
            .distinct(Invoices.supplier_latitude, Invoices.supplier_longitude))
        
        for invoice in query:
            warehouse_coords.append({
                "lat": invoice.supplier_latitude,
                "lon": invoice.supplier_longitude,
                "value": invoice.total_amount,
                "name": invoice.supplier_name,
                })
        
        return {
            "data": warehouse_coords
        }
        
    elif query == "deliveriesMadeMonthly":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)
            query = (LineItems
                    .select(fn.TO_CHAR(Invoices.delivery_date, 'Mon').alias('month'),
                            fn.COUNT('*').alias('count'))
                    .join(Invoices)
                    .where((Invoices.is_valid == True) &
                            (Invoices.owner == owner) &
                            (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                            (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                            Invoices.delivery_date.between(from_date, to_date)
                        )
                    .group_by(fn.TO_CHAR(Invoices.delivery_date, 'Mon'))
                    .order_by(fn.MIN(Invoices.delivery_date)))
        else:
            query = (LineItems
                .select(fn.TO_CHAR(Invoices.delivery_date, 'Mon').alias('month'),
                        fn.COUNT('*').alias('count'))
                .join(Invoices)
                .where((Invoices.is_valid == True) &
                        (Invoices.owner == owner) &
                        Invoices.delivery_date.between(from_date, to_date)
                    )
                .group_by(fn.TO_CHAR(Invoices.delivery_date, 'Mon'))
                .order_by(fn.MIN(Invoices.delivery_date)))

        result = query.dicts()
        labels = [item['month'] for item in result]
        data = [item['count'] for item in result]

        return {
            "labels": labels,
            "data": data
        }
        
    elif query == "warehouseMonthlyAvgDeliveryTime":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)
            query = (Invoices
                .select(fn.TO_CHAR(Invoices.delivery_date, 'Mon').alias('month'),
                        fn.AVG(Invoices.delivery_date - Invoices.invoice_start_date).alias('average_delivery_time'))
                .where((Invoices.is_valid == True) &
                        (Invoices.owner == owner) &
                        (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                        (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                        Invoices.delivery_date.between(from_date, to_date))
                .group_by(fn.TO_CHAR(Invoices.delivery_date, 'Mon'))
                .order_by(fn.MIN(Invoices.delivery_date)))
        else:
            query = (Invoices
                .select(fn.TO_CHAR(Invoices.delivery_date, 'Mon').alias('month'),
                        fn.AVG(Invoices.delivery_date - Invoices.invoice_start_date).alias('average_delivery_time'))
                .where((Invoices.is_valid == True) &
                        (Invoices.owner == owner) &
                        Invoices.delivery_date.between(from_date, to_date))
                .group_by(fn.TO_CHAR(Invoices.delivery_date, 'Mon'))
                .order_by(fn.MIN(Invoices.delivery_date)))
    
        result = query.dicts()
        labels = [item['month'] for item in result]
        data = [item['average_delivery_time'] for item in result]
        
        return {
            "labels": labels,
            "data": data
        }
        
    elif query == "warehouseMonthlyAvgDeliveryDistance":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)
            invoices = (
                Invoices.select(
                    Invoices.delivery_date,
                    Invoices.supplier_latitude,
                    Invoices.supplier_longitude,
                    Invoices.delivery_latitude,
                    Invoices.delivery_longitude,
                )
                .where(
                    (Invoices.is_valid == True) &
                    (Invoices.owner == owner) &
                    (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                    (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                    (Invoices.delivery_date >= from_date) &
                    (Invoices.delivery_date <= to_date)
                )
                .order_by(Invoices.delivery_date)
            )
        else:
            invoices = (
                Invoices.select(
                    Invoices.delivery_date,
                    Invoices.supplier_latitude,
                    Invoices.supplier_longitude,
                    Invoices.delivery_latitude,
                    Invoices.delivery_longitude,
                )
                .where(
                    (Invoices.is_valid == True) &
                    (Invoices.owner == owner) &
                    (Invoices.delivery_date >= from_date)
                    & (Invoices.delivery_date <= to_date)
                )
                .order_by(Invoices.delivery_date)
            )

        monthly_distances = defaultdict(list)
        for invoice in invoices:
            month = invoice.delivery_date.strftime("%b")
            distance = coord_distance(
                invoice.supplier_latitude,
                invoice.supplier_longitude,
                invoice.delivery_latitude,
                invoice.delivery_longitude,
            )
            monthly_distances[month].append(distance)

        avg_monthly_distances = {
            month: sum(distances) / len(distances)
            for month, distances in monthly_distances.items()
        }

        result = {
            "labels": list(avg_monthly_distances.keys()),
            "data": list(avg_monthly_distances.values()),
        }
        return result
    
    elif query == "numUniqueCustomers":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)

            # Query the database for active customers within the date range
            active_customers = Invoices.select().where(
                (Invoices.is_valid == True) &
                (Invoices.invoice_end_date >= from_date) &
                (Invoices.invoice_end_date <= to_date) &
                (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                (Invoices.owner == owner)
            ).distinct(Invoices.customer_name)

            # Count the number of active customers
            num_active_customers = active_customers.count()

            # Define the date range to query for the previous 12 months
            prev_year_to_date = to_date - timedelta(days=365)
            prev_year_from_date = prev_year_to_date - timedelta(days=90)

            # Query the database for active customers within the previous 12 months
            prev_year_active_customers = Invoices.select().where(
                (Invoices.is_valid == True) &
                (Invoices.invoice_end_date >= prev_year_from_date) &
                (Invoices.invoice_end_date <= prev_year_to_date) &
                (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE) &
                (Invoices.owner == owner)
            ).distinct(Invoices.customer_name)

            # Count the number of active customers in the previous 12 months
            num_prev_year_active_customers = prev_year_active_customers.count()

            # Calculate the percentage change in active customers from the previous 12 months
            if num_prev_year_active_customers == 0:
                percentage_change = 0
            else:
                percentage_change = ((num_active_customers - num_prev_year_active_customers) / num_prev_year_active_customers) * 100

            return {
                "value": num_active_customers,
                "change": percentage_change,
            }
        else:
            # Query the database for active customers within the date range
            active_customers = Invoices.select().where(
                (Invoices.is_valid == True) &
                (Invoices.invoice_end_date >= from_date) &
                (Invoices.invoice_end_date <= to_date) &
                (Invoices.owner == owner)
            ).distinct(Invoices.customer_name)

            # Count the number of active customers
            num_active_customers = active_customers.count()

            # Define the date range to query for the previous 12 months
            prev_year_to_date = to_date - timedelta(days=365)
            prev_year_from_date = prev_year_to_date - timedelta(days=90)

            # Query the database for active customers within the previous 12 months
            prev_year_active_customers = Invoices.select().where(
                (Invoices.is_valid == True) &
                (Invoices.invoice_end_date >= prev_year_from_date) &
                (Invoices.invoice_end_date <= prev_year_to_date) &
                (Invoices.owner == owner)
            ).distinct(Invoices.customer_name)

            # Count the number of active customers in the previous 12 months
            num_prev_year_active_customers = prev_year_active_customers.count()

            # Calculate the percentage change in active customers from the previous 12 months
            if num_prev_year_active_customers == 0:
                percentage_change = 0
            else:
                percentage_change = ((num_active_customers - num_prev_year_active_customers) / num_prev_year_active_customers) * 100

            return {
                "value": num_active_customers,
                "change": percentage_change,
            }
    elif query == "totalRevenue":
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        
        if warehouse_lat and warehouse_long:
            warehouse_lat = float(warehouse_lat)
            warehouse_long = float(warehouse_long)
            
            invoices = (
                Invoices.select(
                    fn.SUM(LineItems.total_price).alias('total_revenue')
                )
                .join(LineItems, on=(Invoices.id == LineItems.invoice))
                .where(
                    (Invoices.delivery_date >= from_date) &
                    (Invoices.delivery_date <= to_date) &
                    (Invoices.is_valid == True) &
                    (Invoices.owner == owner) &
                    (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                    (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE)
                )
            )

            total_revenue = invoices[0].total_revenue if invoices else 0
            
            # Define the date range to query for the previous 12 months
            prev_year_to_date = to_date - timedelta(days=365)
            prev_year_from_date = prev_year_to_date - timedelta(days=90)
            
            prev_year_invoices = (
                Invoices.select(
                    fn.SUM(LineItems.total_price).alias('total_revenue')
                )
                .join(LineItems, on=(Invoices.id == LineItems.invoice))
                .where(
                    (Invoices.delivery_date >= prev_year_from_date) &
                    (Invoices.delivery_date <= prev_year_to_date) &
                    (Invoices.is_valid == True) &
                    (Invoices.owner == owner) &
                    (fn.ABS(Invoices.supplier_latitude - warehouse_lat) <= TOLERANCE) &
                    (fn.ABS(Invoices.supplier_longitude - warehouse_long) <= TOLERANCE)
                )
            )
            
            prev_year_total_revenue = prev_year_invoices[0].total_revenue if prev_year_invoices else 0
            
            # Calculate the percentage change in total revenue from the previous 12 months
            if prev_year_total_revenue == 0:
                percentage_change = 0
            else:
                percentage_change = ((total_revenue - prev_year_total_revenue) / prev_year_total_revenue) * 100
            
            return {
                "value": total_revenue,
                "change": percentage_change,
            }
            
        else:
            invoices = (
                Invoices.select(
                    fn.SUM(LineItems.total_price).alias('total_revenue')
                )
                .join(LineItems, on=(Invoices.id == LineItems.invoice))
                .where(
                    (Invoices.is_valid == True) &
                    (Invoices.owner == owner) &
                    (Invoices.delivery_date >= from_date) &
                    (Invoices.delivery_date <= to_date)
                )
            )

            total_revenue = invoices[0].total_revenue if invoices else 0
            
            # Define the date range to query for the previous 12 months
            prev_year_to_date = to_date - timedelta(days=365)
            prev_year_from_date = prev_year_to_date - timedelta(days=90)
            
            prev_year_invoices = (
                Invoices.select(
                    fn.SUM(LineItems.total_price).alias('total_revenue')
                )
                .join(LineItems, on=(Invoices.id == LineItems.invoice))
                .where(
                    (Invoices.is_valid == True) &
                    (Invoices.owner == owner) &
                    (Invoices.delivery_date >= prev_year_from_date) &
                    (Invoices.delivery_date <= prev_year_to_date)
                )
            )
            
            prev_year_total_revenue = prev_year_invoices[0].total_revenue if prev_year_invoices else 0
            
            # Calculate the percentage change in total revenue from the previous 12 months
            if prev_year_total_revenue == 0:
                percentage_change = 0
            else:
                percentage_change = ((total_revenue - prev_year_total_revenue) / prev_year_total_revenue) * 100
            
            return {
                "value": total_revenue,
                "change": percentage_change,
            }
        
    return {}
