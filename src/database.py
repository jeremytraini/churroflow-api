from peewee import *
import os

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
    name = TextField()
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
    owner = ForeignKeyField(Users, backref='owner', null=True)
    
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

class Invoices(BaseModel):
    name = TextField()
    owner = ForeignKeyField(Users, backref='invoices')
    date_last_modified = DateField()
    date_added = DateField()
    num_warnings = IntegerField()
    num_errors = IntegerField()
    
    is_valid = BooleanField()
    text_content = TextField(null=True,default=None)
    
    invoice_title = TextField(null=True,default=None)
    issue_date = DateField(null=True,default=None)
    due_date = DateField(null=True,default=None)
    order_id = TextField(null=True,default=None)
    invoice_start_date = DateField(null=True,default=None)
    invoice_end_date = DateField(null=True,default=None)
    
    supplier_name = TextField(null=True,default=None)
    supplier_abn = TextField(null=True,default=None)
    supplier_latitude = FloatField(null=True,default=None)
    supplier_longitude = FloatField(null=True,default=None)
    
    customer_name = TextField(null=True,default=None)
    customer_abn = TextField(null=True,default=None)
    
    delivery_date = DateField(null=True,default=None)
    delivery_latitude = FloatField(null=True,default=None)
    delivery_longitude = FloatField(null=True,default=None)
    delivery_suburb = TextField(null=True,default=None)
    
    customer_contact_name = TextField(null=True,default=None)
    customer_contact_email = TextField(null=True,default=None)
    customer_contact_phone = TextField(null=True,default=None)
    
    total_amount = FloatField(null=True,default=None)
    
    def to_json(self, verbose = True):
        if not verbose:
            return {
                "id": self.id,
                "name": self.name,
                "date_last_modified": str(self.date_last_modified),
                "date_added": str(self.date_added),
                "num_warnings": self.num_warnings,
                "num_errors": self.num_errors,
                "is_valid": self.is_valid,
                "invoice_title": self.invoice_title,
            }
        
        return {
            "id": self.id,
            "name": self.name,
            "date_last_modified": str(self.date_last_modified),
            "date_added": str(self.date_added),
            "num_warnings": self.num_warnings,
            "num_errors": self.num_errors,
            "is_valid": self.is_valid,
            "text_content": self.text_content,
            "invoice_title": self.invoice_title,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "order_id": self.order_id,
            "invoice_start_date": str(self.invoice_start_date),
            "invoice_end_date": str(self.invoice_end_date),
            "supplier_name": self.supplier_name,
            "supplier_abn": self.supplier_abn,
            "supplier_latitude": self.supplier_latitude,
            "supplier_longitude": self.supplier_longitude,
            "customer_name": self.customer_name,
            "customer_abn": self.customer_abn,
            "delivery_date": str(self.delivery_date),
            "delivery_latitude": self.delivery_latitude,
            "delivery_longitude": self.delivery_longitude,
            "customer_contact_name": self.customer_contact_name,
            "customer_contact_email": self.customer_contact_email,
            "customer_contact_phone": self.customer_contact_phone,
            "total_amount": self.total_amount,
            "line_items": [line_item.to_json() for line_item in self.line_items]
        }

class LineItems(BaseModel):
    invoice = ForeignKeyField(Invoices, backref='line_items')
    
    description = TextField()
    quantity = IntegerField()
    unit_price = FloatField()
    total_price = FloatField()
    
    def to_json(self):
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price
        }


tables = [Users, Evaluations, Reports, Violations, Sessions, Invoices, LineItems]

# Create the tables in the database
def create_tables():
    with db:
        if db.table_exists('invoices'):
            # add delivery_suburb column to invoices table if it doesn't exist
            db.execute_sql('ALTER TABLE invoices ADD COLUMN IF NOT EXISTS delivery_suburb TEXT NULL DEFAULT NULL;')
            
        db.create_tables(tables)

def clear_v2(token: str):
    session = Sessions.get(token=token)
    
    if session.user.email != "churros@admin.com":
        raise Exception("Only admins can clear the database")
    
    with db:
        db.drop_tables(tables)
        db.create_tables(tables)

# Connect to the database when this file is imported
db.connect()

create_tables()
