from faker import Faker
import random
import datetime
from src.database import Invoices, LineItems, db

# Instantiate a Faker object
fake = Faker()

NUM_INVOICES = 100
NUM_LINE_ITEMS = 300

def random_lat():
    min_lat, max_lat = -34.05, -33.568
    return round(random.uniform(min_lat, max_lat), 6)

def random_lon():
    min_lon, max_lon = 150.52, 151.34
    return round(random.uniform(min_lon, max_lon), 6)

supplier = ("Churros Pty Ltd", "12345678901")
supplier_warehouses = [
    (random_lat(), random_lon()),
    (random_lat(), random_lon()),
    (random_lat(), random_lon()),
]

fake_customers = [(fake.company(),
                   fake.random_number(digits=9),
                   random_lat(),
                   random_lon(),
                   fake.name(),
                   fake.email(),
                   fake.phone_number(),
                   ) for _ in range(20)]

# Generate fake data for the invoices table
invoices = []
for i in range(1, NUM_INVOICES + 1):
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
        ('Pens', 1.00),
        ('Pencils', 0.50),
        ('Paper', 0.10),
        ('Stapler', 5.00),
        ('Staples', 0.05),
        ('Paper Clips', 0.01),
        ('Ruler', 0.50),
        ('Eraser', 0.10),
        ('Glue', 0.50),
        ('Scissors', 1.00),
        ('Tape', 0.50),
        ('Sticky Notes', 0.50),
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
        round(quantity * item[1], 2)
    ))

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
db.drop_tables([Invoices, LineItems])
db.create_tables([Invoices, LineItems])

# Add the fake data to the database
Invoices.insert_many(invoices).execute()
LineItems.insert_many(lineitems).execute()
