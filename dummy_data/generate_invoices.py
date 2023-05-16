from time import sleep
from faker import Faker
import random
import datetime
import binascii
import requests
import sys

# Check for file input and folder input

if len(sys.argv) < 3:
    print("Usage: python3 generate_invoices.py <template_file> <output_folder>")
    sys.exit(1)
    
TEMPLATE_FILE = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]
START_AT = 1

# Instantiate a Faker object
fake = Faker()

NUM_INVOICES = 500
NUM_LINE_ITEMS = 300

weighting = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

def validate(abn):
    """
    Validate that the provided number is indeed an ABN.
    """
    values = list(map(int, list(abn)))
    values[0] -= 1
    total = sum([x * w for (x, w) in zip(values, weighting)])
    return total % 89 == 0

def abn():
    """
    Generate a random ABN
    """
    value = ''.join([str(int(random.random() * 10)) for i in range(9)])
    temp = list('00%s' % value)
    total = sum([w * x for (w,x) in zip(weighting, map(int, temp))])
    remainder = total % 89
    prefix = 10 + (89 - remainder)
    abn = '%s%s' % (prefix, value)
    if not validate(abn):
        return abn()
    return abn

def random_lat():
    min_lat, max_lat = -34.05, -33.568
    return round(random.uniform(min_lat, max_lat), 6)

def random_lon():
    min_lon, max_lon = 150.52, 151.34
    return round(random.uniform(min_lon, max_lon), 6)

supplier = ("Churros Pty Ltd", abn())
supplier_warehouses = [
    (-33.913944, 151.022874),
    (-33.848536, 150.901258),
    (-33.791443, 151.072199),
]

# -33.913944, 151.022874
# -33.848536, 150.901258
# -33.791443, 151.072199

fake_customers = [(fake.company(),
                   abn(),
                   random_lat(),
                   random_lon(),
                   fake.name(),
                   fake.email(),
                   fake.phone_number(),
                   ) for _ in range(20)]

# Generate fake data for the invoices table
invoices = []
for i in range(START_AT, NUM_INVOICES + 1):
    customer = random.choice(fake_customers)
    
    issue_date = fake.date_time_between(start_date="-2y", end_date="now")
    due_date = fake.date_time_between(start_date=issue_date, end_date="now")
    
    start_date = fake.date_time_between(start_date=issue_date - datetime.timedelta(days=30), end_date=issue_date)
    end_date = fake.date_time_between(start_date=start_date, end_date=start_date + datetime.timedelta(days=30))
    
    delivery_date = fake.date_time_between(start_date=start_date, end_date=start_date + datetime.timedelta(days=10))
    
    supplier_warehouse = random.choice(supplier_warehouses)
    
    invoices.append((
        "invoice{}.xml".format(i),
        1,
        fake.date_time_between(start_date="-1d", end_date="now").strftime('%Y-%m-%d'),
        fake.date_time_between(start_date="-1d", end_date="now").strftime('%Y-%m-%d'),
        0,
        0,
        True,
        "",
        "Invoice #{}".format(i),
        issue_date.strftime('%Y-%m-%d'),
        due_date.strftime('%Y-%m-%d'),
        random.randint(1, 100),
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        supplier[0],
        supplier[1],
        supplier_warehouse[0],
        supplier_warehouse[1],
        customer[0],
        customer[1],
        delivery_date.strftime('%Y-%m-%d'),
        # random_lat(),
        # random_lon(),
        round(random.uniform(supplier_warehouse[0], customer[2]), 6),
        round(random.uniform(supplier_warehouse[1], customer[3]), 6),
        # customer[2],
        # customer[3],
        customer[4],
        customer[5],
        customer[6],
        round(random.uniform(100, 10000), 2)
    ))

# List of stationary supply items and their price
possible_items = [
        ('Pens', 1000.00),
        ('Pencils', 1000.00),
        ('Paper', 0.10),
        ('Stapler', 5.00),
        ('Staples', 1.00),
        ('Paper Clips', 1.00),
        ('Ruler', 0.50),
        ('Eraser', 0.10),
        ('Glue', 3.00),
        ('Scissors', 6.00),
        ('Tape', 5.00),
        ('Sticky Notes', 4.00),
]

# Generate fake data for the lineitems table
lineitems = []
for i in range(1, NUM_LINE_ITEMS + 1):
    item = random.choice(possible_items)
    quantity = random.randint(1, 10)
    
    lineitems.append((
        random.randint(1, NUM_INVOICES),
        item[0],
        quantity,
        item[1],
        # round(quantity * item[1], 2)
        random.randint(50, 500)
    ))
    


TEMPLATE_INVOICE = None
with open(TEMPLATE_FILE, 'r') as f:
    TEMPLATE_INVOICE = f.read()

def get_address_data(lat, lon):
    sleep(0.5)
    
    addy = requests.get(f"https://geocode.maps.co/reverse", params={
        "lat": str(lat),
        "lon": str(lon),
    }).json()['address']
    
    for key in ['road', 'suburb', 'postcode', 'country']:
        if key not in addy:
            return False
    
    return addy

addresses = []
for i in range(3):
    addy = get_address_data(supplier_warehouses[i][0], supplier_warehouses[i][1])
    while not addy:
        print('retrying')
        addy = get_address_data(supplier_warehouses[i][0], supplier_warehouses[i][1])
    addresses.append(addy)

# supplier_warehouses
warehouse_addresses = {
    supplier_warehouses[0][0]: addresses[0],
    supplier_warehouses[1][0]: addresses[1],
    supplier_warehouses[2][0]: addresses[2],
}


for invoice in invoices:
    print('supplier coords', invoice[16], invoice[17])
    print('delivery coords', invoice[21], invoice[22])
    
    # supplier_address_data = random.choice(warehouse_addresses)
    supplier_address_data = warehouse_addresses[invoice[16]]
        
    # flag = False
    # for key in ['road', 'postcode', 'country']:
    #     if key not in supplier_address_data:
    #         flag = True
    # if flag:
    #     continue
    
    delivery_address_data = get_address_data(invoice[21], invoice[22])
    
    if not delivery_address_data:
        continue
    # flag = False
    # for key in ['road', 'postcode', 'country']:
    #     if key not in delivery_address_data:
    #         flag = True
    # if flag:
    #     continue
    
    # if supplier_address_data['road'] == delivery_address_data['road']:
    #     print('Same road' + supplier_address_data['road'])
    #     continue
    
    with open(f'{OUTPUT_FOLDER}/{invoice[0]}', 'w') as f:
        invoice_text = TEMPLATE_INVOICE
        supplier_road = supplier_address_data["road"]
        supplier_suburb = supplier_address_data["suburb"]
        supplier_city = supplier_address_data["city"]
        supplier_state = supplier_address_data["state"]
        supplier_postcode = supplier_address_data["postcode"]
        supplier_country = supplier_address_data["country"]
        
        delivery_road = delivery_address_data["road"]
        delivery_suburb = delivery_address_data["suburb"] if "suburb" in delivery_address_data else ""
        delivery_city = delivery_address_data["city"] if "city" in delivery_address_data else ""
        delivery_state = delivery_address_data["state"] if "state" in delivery_address_data else ""
        delivery_postcode = delivery_address_data["postcode"]
        
        invoice_text = invoice_text.replace("{{name}}", invoice[8])
        invoice_text = invoice_text.replace("{{issue_date}}", invoice[9])
        invoice_text = invoice_text.replace("{{due_date}}", invoice[10])
        invoice_text = invoice_text.replace("{{order_id}}", str(invoice[11]))
        invoice_text = invoice_text.replace("{{invoice_start_date}}", invoice[12])
        invoice_text = invoice_text.replace("{{invoice_end_date}}", invoice[13])
        invoice_text = invoice_text.replace("{{supplier_name}}", invoice[14])
        invoice_text = invoice_text.replace("{{supplier_abn}}", invoice[15])
        invoice_text = invoice_text.replace("{{order_ref}}", 'CF%06X' % random.randint(0, 256**3-1))
        
        invoice_text = invoice_text.replace("{{supplier_road}}", supplier_road)
        invoice_text = invoice_text.replace("{{supplier_suburb}}", supplier_suburb if supplier_suburb else "")
        invoice_text = invoice_text.replace("{{supplier_city}}", supplier_city if supplier_city else "")
        invoice_text = invoice_text.replace("{{supplier_state}}", supplier_state if supplier_state else "")
        invoice_text = invoice_text.replace("{{supplier_postcode}}", supplier_postcode)
        invoice_text = invoice_text.replace("{{supplier_country}}", "Australia")
        
        invoice_text = invoice_text.replace("{{customer_name}}", invoice[18])
        invoice_text = invoice_text.replace("{{customer_abn}}", str(invoice[19]))
        invoice_text = invoice_text.replace("{{delivery_date}}", invoice[20])
        
        invoice_text = invoice_text.replace("{{delivery_road}}", delivery_road)
        invoice_text = invoice_text.replace("{{delivery_suburb}}", delivery_suburb)
        invoice_text = invoice_text.replace("{{delivery_city}}", delivery_city)
        invoice_text = invoice_text.replace("{{delivery_state}}", delivery_state)
        invoice_text = invoice_text.replace("{{delivery_postcode}}", delivery_postcode)
        invoice_text = invoice_text.replace("{{delivery_country}}", "Australia")
        
        invoice_text = invoice_text.replace("{{customer_contact_name}}", invoice[23])
        invoice_text = invoice_text.replace("{{customer_contact_email}}", invoice[24])
        invoice_text = invoice_text.replace("{{customer_contact_phone}}", invoice[25])
        
        
        line_item = random.choice(lineitems)
        
        # description,quantity,unit_price,total_price
        invoice_text = invoice_text.replace("{{description}}", line_item[1])
        
        
        pre_tax_total = line_item[4]
        tax_amount = round(pre_tax_total * 0.1, 2)
        total_amount = round(pre_tax_total + tax_amount, 2)
        
        invoice_text = invoice_text.replace("{{pre_tax_total}}", str(pre_tax_total))
        invoice_text = invoice_text.replace("{{tax_amount}}", str(tax_amount))
        invoice_text = invoice_text.replace("{{total_amount}}", str(total_amount))
        
        f.write(invoice_text)
        # break

# save the fake data to a csv
# with open('invoices.csv', 'w') as f:
#     f.write("id,name,owner_id,date_last_modified,date_added,num_warnings,num_errors,is_valid,text_content,invoice_title,issue_date,due_date,order_id,invoice_start_date,invoice_end_date,supplier_name,supplier_abn,supplier_latitude,supplier_longitude,customer_name,customer_abn,delivery_date,delivery_latitude,delivery_longitude,customer_contact_name,customer_contact_email,customer_contact_phone,total_amount")
#     for invoice in invoices:
#         f.write(f"\n{','.join(str(x) for x in invoice)}")
    
# with open('lineitems.csv', 'w') as f:
#     f.write("id,invoice_id,description,quantity,unit_price,total_price")
#     for lineitem in lineitems:
#         f.write(f"\n{','.join(str(x) for x in lineitem)}")

# Clear Invoices and LineItems tables
# db.drop_tables([Invoices, LineItems])
# db.create_tables([Invoices, LineItems])

# # Add the fake data to the database
# Invoices.insert_many(invoices).execute()
# LineItems.insert_many(lineitems).execute()

