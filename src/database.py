from peewee import *
import os
from src.constants import ADMIN_TOKEN

db = None
if 'RDS_DB_NAME' in os.environ:
    db = PostgresqlDatabase(os.environ['RDS_DB_NAME'],
                            host=os.environ['RDS_HOSTNAME'],
                            port=os.environ['RDS_PORT'],
                            user=os.environ['RDS_USERNAME'],
                            password=os.environ['RDS_PASSWORD'])
else:
    db = PostgresqlDatabase(os.environ['POSTGRES_DB'],
                            host=os.environ['POSTGRES_HOST'],
                            port=os.environ['POSTGRES_PORT'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'])
    
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
        violations = Violations.select().where(Violations.evaluation == self.id) # type: ignore
        
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
    invoice_text = TextField(null=True, default=None)
    invoice_hash = TextField()
    is_valid = BooleanField()
    total_warnings = IntegerField()
    total_errors = IntegerField()
    wellformedness = ForeignKeyField(Evaluations, backref='wellformedness')
    schema = ForeignKeyField(Evaluations, backref='schema', null=True, default=None)
    syntax = ForeignKeyField(Evaluations, backref='syntax', null=True, default=None)
    peppol = ForeignKeyField(Evaluations, backref='peppol', null=True, default=None)
    owner = ForeignKeyField(Users, backref='users', null=True)
    
    def to_json(self):
        return {
            "report_id": self.id, # type: ignore
            "date_generated": str(self.date_generated),
            "invoice_name": self.invoice_name,
            "invoice_hash": self.invoice_hash,
            "is_valid": self.is_valid,
            "total_warnings": self.total_warnings,
            "total_errors": self.total_errors,
            "wellformedness_evaluation": self.wellformedness.to_json(),
            "schema_evaluation": self.schema.to_json() if self.schema else None,
            "syntax_evaluation": self.syntax.to_json() if self.syntax else None,
            "peppol_evaluation": self.peppol.to_json() if self.peppol else None
        }


class Violations(BaseModel):
    evaluation = ForeignKeyField(Evaluations, backref='violations', null=True, default=None)
    rule_id = TextField()
    is_fatal = BooleanField()
    message = TextField(null=True, default=None)
    suggestion = TextField(null=True, default=None)
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

def clear_v1(token: str):
    if not token == ADMIN_TOKEN:
        raise Exception("Only admins can clear the database")
    
    with db:
        db.drop_tables(tables)
        db.create_tables(tables)

# Connect to the database when this file is imported
db.connect()

create_tables()
