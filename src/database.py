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
    is_valid = BooleanField()
    num_warnings = IntegerField()
    num_errors = IntegerField()
    num_rules_failed = IntegerField()
    
    def to_json(self):
        violations = Violations.select().where(Violations.evaluation == self.id)
        
        return {
            "is_valid": self.is_valid,
            "num_warnings": self.num_warnings,
            "num_errors": self.num_errors,
            "num_rules_failed": self.num_rules_failed,
            "violations": [violation.to_json() for violation in violations]
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
    
    def to_json(self):
        return {
            "date_generated": self.date_generated,
            "invoice_name": self.invoice_name,
            "invoice_raw": self.invoice_raw,
            "invoice_hash": self.invoice_hash,
            "is_valid": self.is_valid,
            "total_warnings": self.total_warnings,
            "total_errors": self.total_errors,
            "wellformedness": self.wellformedness.to_json(),
            "schema": self.schema.to_json() if self.schema else None,
            "syntax": self.syntax.to_json() if self.syntax else None,
            "peppol": self.peppol.to_json() if self.peppol else None
        }


class Violations(BaseModel):
    evaluation = ForeignKeyField(Evaluations, backref='violations', null=True, default=None)
    rule_id = TextField()
    is_fatal = BooleanField()
    message = TextField()
    suggestion = TextField()
    test = TextField(null=True, default=None)
    xpath = TextField(null=True, default=None)
    line = IntegerField(null=True, default=None)
    column = IntegerField(null=True,default=None)
    
    def to_json(self):
        return {
            "rule_id": self.rule_id,
            "is_fatal": self.is_fatal,
            "message": self.message,
            "suggestion": self.suggestion,
            "test": self.test,
            "xpath": self.xpath,
            "line": self.line,
            "column": self.column
        }


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
