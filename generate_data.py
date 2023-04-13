from faker import Faker
import random
import datetime

# Instantiate a Faker object
fake = Faker()

def random_lat():
    min_lat, max_lat = -34.05, -33.568
    return round(random.uniform(min_lat, max_lat), 6)

def random_lon():
    min_lon, max_lon = 150.52, 151.34
    return round(random.uniform(min_lon, max_lon), 6)

# Generate fake data for the invoices table
invoices = []
for i in range(1, 101):
    invoices.append((
        i,
        fake.company(),
        random.randint(1, 10),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d %H:%M:%S'),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d %H:%M:%S'),
        random.randint(0, 10),
        random.randint(0, 10),
        random.choice([True, False]),
        fake.text(),
        fake.text(),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d'),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d'),
        random.randint(1, 100),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d'),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d'),
        fake.company(),
        fake.random_number(digits=9),
        random_lat(),
        random_lon(),
        fake.company(),
        fake.random_number(digits=9),
        fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%d'),
        random_lat(),
        random_lon(),
        fake.name(),
        fake.email(),
        fake.phone_number(),
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
    
    lineitems.append((
        i,
        random.randint(1, 100),
        item[0],
        random.randint(1, 10),
        round(random.uniform(10, 100), 2),
        0
    ))

    # Calculate total_price
    lineitems[-1] = lineitems[-1][:5] + (lineitems[-1][3] * lineitems[-1][4],)

# Output the fake data
print("INSERT INTO invoices (id, name, owner_id, date_last_modified, date_added, num_warnings, num_errors, is_valid, text_content, invoice_title, issue_date, due_date, order_id, invoice_start_date, invoice_end_date, supplier_name, supplier_abn, supplier_latitude, supplier_longitude, customer_name, customer_abn, delivery_date, delivery_latitude, delivery_longitude, customer_contact_name, customer_contact_email, customer_contact_phone, total_amount) VALUES")
print(",\n".join(str(invoice) for invoice in invoices))

print("\n\nINSERT INTO lineitems (id, invoice_id, description, quantity, unit_price, total_price) VALUES")
print(",\n".join(str(lineitem) for lineitem in lineitems))