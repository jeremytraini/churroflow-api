from peewee import *


db = PostgresqlDatabase('validation', host='localhost', port=5433, user='postgres', password='postgres')


# Defining database models using Peewee's Model class
class Users(Model):
    email = TextField(unique=True)
    password_hash = TextField()

    class Meta:
        database=db
        db_table='Users'

class Evaluations(Model):
    num_violations = IntegerField()
    num_warnings = IntegerField()
    num_errors = IntegerField()

    class Meta:
        database=db
        db_table='Evaluations'


class Reports(Model):
    date_generated = DateTimeField()
    invoice_name = TextField()
    invoice_raw = TextField()
    invoice_hash = TextField()
    is_valid = BooleanField()
    total_violations = IntegerField()
    total_warnings = IntegerField()
    total_errors = IntegerField()
    wellformedness = ForeignKeyField(Evaluations, backref='wellformedness')
    schema = ForeignKeyField(Evaluations, backref='schema')
    syntax = ForeignKeyField(Evaluations, backref='syntax')
    peppol = ForeignKeyField(Evaluations, backref='peppol')

    class Meta:
        database=db
        db_table='Reports'


class Violations(Model):
    evaluation = ForeignKeyField(Evaluations, backref='violations')
    rule_id = TextField()
    is_fatal = BooleanField()
    message = TextField()
    test = TextField()
    xpath = TextField()
    line = IntegerField()
    column = IntegerField()

    class Meta:
        database=db
        db_table='Violations'

# Create the tables in the database
def create_tables():
    with db:
        db.create_tables([Users, Evaluations, Reports, Violations])

# Connect to the database when this file is imported
db.connect()

create_tables()

print(db.get_tables())
