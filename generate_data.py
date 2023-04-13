from faker import Faker
import random
import datetime
from src.database import db

# Instantiate a Faker object
fake = Faker()

def random_lat():
    min_lat, max_lat = -34.05, -33.568
    return round(random.uniform(min_lat, max_lat), 6)

def random_lon():
    min_lon, max_lon = 150.52, 151.34
    return round(random.uniform(min_lon, max_lon), 6)

supplier = ("Churros Pty Ltd", "12345678901", random_lat(), random_lon())

fake_customers = [(fake.company(),
                   fake.random_number(digits=9),
                   random_lat(),
                   random_lon(),
                   fake.name(),
                   fake.email(),
                   fake.phone_number(),
                   ) for i in range(20)]

# Generate fake data for the invoices table
invoices = []
for i in range(1, 101):
    customer = random.choice(fake_customers)
    
    issue_date = fake.date_time_between(start_date="-2y", end_date="now")
    due_date = fake.date_time_between(start_date=issue_date, end_date="now")
    
    start_date = fake.date_time_between(start_date=issue_date - datetime.timedelta(days=30), end_date=issue_date)
    end_date = fake.date_time_between(start_date=start_date, end_date=start_date + datetime.timedelta(days=30))
    
    delivery_date = fake.date_time_between(start_date=start_date, end_date=start_date + datetime.timedelta(days=10))
    
    invoices.append((
        i,
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
        supplier[2],
        supplier[3],
        customer[0],
        customer[1],
        delivery_date.strftime('%Y-%m-%d'),
        customer[2],
        customer[3],
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
for i in range(1, 1001):
    item = random.choice(possible_items)
    quantity = random.randint(1, 10)
    
    lineitems.append((
        i,
        random.randint(1, 100),
        item[0],
        quantity,
        item[1],
        round(quantity * item[1], 2)
    ))

    # Calculate total_price
    # lineitems[-1] = lineitems[-1][:5] + (lineitems[-1][3] * lineitems[-1][4],)

# Output the fake data
# print("INSERT INTO invoices (id, name, owner_id, date_last_modified, date_added, num_warnings, num_errors, is_valid, text_content, invoice_title, issue_date, due_date, order_id, invoice_start_date, invoice_end_date, supplier_name, supplier_abn, supplier_latitude, supplier_longitude, customer_name, customer_abn, delivery_date, delivery_latitude, delivery_longitude, customer_contact_name, customer_contact_email, customer_contact_phone, total_amount) VALUES")
# print(",\n".join(str(invoice) for invoice in invoices))

# print("\n\nINSERT INTO lineitems (id, invoice_id, description, quantity, unit_price, total_price) VALUES")
# print(",\n".join(str(lineitem) for lineitem in lineitems))

# save the fake data to a csv
with open('invoices.csv', 'w') as f:
    f.write("id,name,owner_id,date_last_modified,date_added,num_warnings,num_errors,is_valid,text_content,invoice_title,issue_date,due_date,order_id,invoice_start_date,invoice_end_date,supplier_name,supplier_abn,supplier_latitude,supplier_longitude,customer_name,customer_abn,delivery_date,delivery_latitude,delivery_longitude,customer_contact_name,customer_contact_email,customer_contact_phone,total_amount")
    for invoice in invoices:
        f.write(f"\n{','.join(str(x) for x in invoice)}")
    
with open('lineitems.csv', 'w') as f:
    f.write("id,invoice_id,description,quantity,unit_price,total_price")
    for lineitem in lineitems:
        f.write(f"\n{','.join(str(x) for x in lineitem)}")



