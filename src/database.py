from peewee import *


db = PostgresqlDatabase('validation', host='localhost', port=5433, user='postgres', password='postgres')

# Defining database models using Peewee's Model class

class BaseModel(Model):
   class Meta:
      database = db

class Users(BaseModel):
    email = TextField(unique=True)
    password_hash = TextField()

class Evaluations(BaseModel):
    num_warnings = IntegerField()
    num_errors = IntegerField()
    num_rules_failed = IntegerField()
    
    def to_json(self):
        return {
            "aspect": self.aspect,
            "is_valid": self.is_valid,
            "num_warnings": self.num_warnings,
            "num_errors": self.num_errors,
            "num_rules_failed": self.num_rules_failed,
            "violations": []
        }

class Reports(BaseModel):
    date_generated = DateTimeField()
    invoice_name = TextField()
    invoice_raw = TextField()
    invoice_hash = TextField()
    is_valid = BooleanField()
    total_warnings = IntegerField()
    total_errors = IntegerField()
    wellformedness = ForeignKeyField(Evaluations, backref='wellformedness')
    schema = ForeignKeyField(Evaluations, backref='schema', null=True, default=None)
    syntax = ForeignKeyField(Evaluations, backref='syntax', null=True, default=None)
    peppol = ForeignKeyField(Evaluations, backref='peppol', null=True, default=None)


class Violations(BaseModel):
    evaluation = ForeignKeyField(Evaluations, backref='violations', null=True, default=None)
    rule_id = TextField()
    is_fatal = BooleanField()
    message = TextField()
    test = TextField(null=True, default=None)
    xpath = TextField(null=True, default=None)
    line = IntegerField(null=True, default=None)
    column = IntegerField(null=True,default=None)


class Sessions(BaseModel):
    user = ForeignKeyField(Users, backref='sessions')
    token = TextField(unique=True)
    date_created = DateTimeField()
    date_expires = DateTimeField()

tables = [Users, Evaluations, Reports, Violations, Sessions]

# Create the tables in the database
def create_tables():
    with db:
        db.create_tables(tables)

def clear_database():
    with db:
        db.drop_tables(tables)
        db.create_tables(tables)

# Connect to the database when this file is imported
db.connect()

create_tables()
# clear_database()
