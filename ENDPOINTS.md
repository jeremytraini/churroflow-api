# ChurroFlow API Endpoints Documentation

Welcome to the ChurroFlow API Endpoints documentation. This document provides a comprehensive guide to all the available API endpoints, required parameters, expected responses, and error codes.

## **Table of Contents**
- [Health Check](#health-check)
- [Authentication](#authentication)
- [Invoice Operations](#invoice-operations)
- [Report Operations](#report-operations)
- [Export](#export)
- [Invoice Processing](#invoice-processing)
- [Admin Operations](#admin-operations)

---

## **Health Check**

### **GET** `/health_check/v1`

**Purpose**: Checks the aliveness of the service.

- **Parameters**: None
- **Response**:
```json
{ "is_alive": true }
```

---

## **Authentication**

### **POST** `/auth/register/v2`

**Purpose**: Registers a new user.

- **Parameters**:
  - `name`: (string) User's name
  - `email`: (string) User's email address
  - `password`: (string) User's password
  
- **Response**:
```json
{ "token": "your_token_here" }
```

- **Errors**:
  - 400: Invalid email, Email already in use, Password shorter than 6 characters.

### **POST** `/auth/login/v2`

**Purpose**: Authenticates and logs in a registered user.

- **Parameters**:
  - `email`: (string) User's email address
  - `password`: (string) User's password

- **Response**:
```json
{ "token": "your_token_here" }
```

- **Errors**:
  - 400: Email not registered, Incorrect password.

### **POST** `/auth/logout/v2`

**Purpose**: Invalidates an active token to log the user out.

- **Parameters**:
  - `token`: (string) Active user token

- **Response**:
```json
{}
```

---

## **Invoice Operations**

### **POST** `/invoice/upload_text/v2`

**Purpose**: Uploads an invoice in text format, generates a validation report.

- **Parameters**:
  - `token`: (string) User's token
  - `invoice`: (dictionary) Invoice details

- **Response**:
```json
{ "report_id": "generated_report_id" }
```

- **Errors**:
  - 400: Name longer than 100 characters
  - 402: Invalid token

---

### **POST** `/invoice/upload_url/v2`

**Purpose**: This endpoint allows users to upload an invoice by providing its URL. The system will then retrieve the invoice from the given URL, validate its contents, and generate a validation report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice` (dictionary): Contains `source` which should be set to "url" and `data` which should be the actual URL of the invoice.

- **Response**:
```json
{
  "report_id": 12345  // Unique identifier for the generated report.
}
```

- **Errors**:
  - 400: 
    - URL is malformed.
    - URL does not point to plain text or XML data.
    - Invoice name exceeds 100 characters.
  - 402: Invalid token.

---

### **POST** `/invoice/upload_file/v2`

**Purpose**: Users can directly upload an XML invoice file. The system will validate the contents of the uploaded XML file and generate a validation report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - File upload: The XML invoice file to be validated.

- **Response**:
```json
{
  "report_id": 12345  // Unique identifier for the generated report.
}
```

- **Errors**:
  - 400: 
    - File does not have a ".xml" extension.
    - Filename exceeds 100 characters.
  - 402: Invalid token.

---

### **POST** `/invoice/file_upload_bulk/v2`

**Purpose**: For users who want to validate multiple invoices at once, this endpoint allows the bulk upload of multiple invoice files. Each invoice will be processed, and a validation report will be generated for each.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoices` (list): A list of invoice dictionaries, each containing details such as `name`, `source` (should be "file" for this endpoint), and `data` which is the actual content of the invoice.

- **Response**:
```json
{
  "report_ids": [12345, 12346, ...]  // A list of unique identifiers for the generated reports.
}
```

- **Errors**:
  - 400: 
    - Any of the provided invoices are in an incorrect format.
  - 402: Invalid token.

---

## **Report Operations**

### **POST** `/report/wellformedness/v2`

**Purpose**: Returns an evaluation on the wellformedness of the given invoice.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice` (dictionary): Invoice details as specified in the Input/Output Types section.

- **Response**:
```json
{
  "evaluation": { ... }  // Evaluation details structure.
}
```

- **Errors**:
  - 400: Invoice in invalid format.
  - 402: Invalid token.

---

### **POST** `/report/schema/v2`

**Purpose**: Validates the schema of a given invoice to ensure it adheres to the expected structure.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice` (dictionary): The invoice data to be validated.

- **Response**:
```json
{
  "evaluation": {...}  // Detailed evaluation of schema validation.
}
```

- **Errors**:
  - 400: 
    - Invoice is in an invalid format.
    - Invoice is not wellformed.
  - 402: Invalid token.

---

### **POST** `/report/syntax/v2`

**Purpose**: Validates the syntax and conformity of the invoice to the EN16931 business rules.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice` (dictionary): The invoice data to be validated.

- **Response**:
```json
{
  "evaluation": {...}  // Detailed evaluation of syntax validation.
}
```

- **Errors**:
  - 400: 
    - Invoice is in an invalid format.
    - Invoice is not wellformed.
    - Invoice has schema errors.
  - 402: Invalid token.

---

### **POST** `/report/peppol/v2`

**Purpose**: Validates the conformance of an invoice to PEPPOL standards.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice` (dictionary): The invoice data to be validated.

- **Response**:
```json
{
  "evaluation": {...}  // Detailed evaluation of PEPPOL conformance.
}
```

- **Errors**:
  - 400: 
    - Invoice is in an invalid format.
    - Invoice is not wellformed.
    - Invoice has schema errors.
  - 402: Invalid token.

---

### **GET** `/report/list_all/v2`

**Purpose**: Retrieves a list of all reports generated by the user.

- **Parameters**:
  - `token` (string): User's authentication token.

- **Response**:
```json
{
  "report_ids": [12345, 12346, ...]  // A list of unique identifiers for the reports.
}
```

- **Errors**:
  - 402: Invalid token.

---

### **GET** `/report/list_by/v2`

**Purpose**: Retrieves a list of reports based on a specific attribute (e.g., `date_generated`).

- **Parameters**:
  - `token` (string): User's authentication token.
  - `order_by` (dictionary): Criteria for ordering the list.

- **Response**:
```json
{
  "report_ids": [12345, 12346, ...]  // Ordered list of unique identifiers for the reports.
}
```

- **Errors**:
  - 400: 
    - `order_by` attribute is not in a valid format.
  - 402: Invalid token.

---

### **PUT** `/report/change_name/v2`

**Purpose**: Updates the name of the invoice contained in a specified report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_id` (integer): ID of the report to be updated.
  - `new_name` (string): New name for the invoice.

- **Response**:
```json
{}  // Empty response indicating successful update.
```

- **Errors**:
  - 400: 
    - `report_id` is less than 1.
    - New name is longer than 100 characters.
  - 402: Invalid token.
  - 404: `report_id` does not exist.

---

### **DELETE** `/report/delete/v2`

**Purpose**: Deletes a specific report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_id` (integer): ID of the report to be deleted.

- **Response**:
```json
{}  // Empty response indicating successful deletion.
```

- **Errors**:
  - 400: 
    - `report_id` is less than 1.
  - 402: Invalid token.
  - 404: `report_id` does not exist.

---

### **GET** `/report/check_validity/v1`

**Purpose**: Checks the validity of an invoice in a specified report.

- **Parameters**:
  - `report_id` (integer): ID of the report to check.

- **Response**:
```json
{
  "is_valid": true,
  "invoice_hash": "abcdef12345..."  // Hash of the invoice.
}
```

- **Errors**:
  - 400: 
    - `report_id` is less than 1.
  - 402: Invalid token.
  - 404: `report_id` does not exist.

---

### **POST** `/report/bulk_export/v2`

**Purpose**: Exports multiple reports in a specified format (e.g., HTML, PDF).

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_ids` (list): List of report IDs to be exported.
  - `report_format` (string): Desired format for the exported reports.

- **Response**:
```json
{
  "reports": [...]  // List of exported reports.
}
```

- **Errors**:
  - 400: 
    - Any `report_id` is less than 1.
    - Invalid `report_format`.
  - 402: Invalid token.
  - 404: Any `report_id` does not exist.


## **Export**

### **GET** `/export/json_report/v2`

**Purpose**: Fetches a complete validation report in JSON format using the provided `report_id`.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_id` (integer): ID of the report to retrieve.

- **Response**:
```json
{
  "report": { ... }  // Detailed report structure.
}
```

- **Errors**:
  - 400: Report ID not found.
  - 402: Invalid token or Unauthorized access to report.

### **GET** `/export/pdf_report/v2`

**Purpose**: Retrieves a PDF report with visual data from the generated validation report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_id` (integer): ID of the report to retrieve.

- **Response**:
  
  Returns a PDF file containing the validation report.

- **Errors**:
  - 400: Report ID not found.
  - 402: Invalid token or Unauthorized access to report.

### **GET** `/export/html_report/v2`

**Purpose**: Retrieves an HTML report with visual data from the generated validation report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_id` (integer): ID of the report to retrieve.

- **Response**:
  
  Returns an HTML file containing the validation report.

- **Errors**:
  - 400: Report ID not found.
  - 402: Invalid token or Unauthorized access to report.

### **GET** `/export/csv_report/v2`

**Purpose**: Retrieves a CSV report with data from the generated validation report.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `report_id` (integer): ID of the report to retrieve.

- **Response**:
  
  Returns a CSV file containing the validation report data.

- **Errors**:
  - 400: Report ID not found.
  - 402: Invalid token or Unauthorized access to report.

---

## **Invoice Processing**

---

### **POST** `/invoice_processing/upload_file/v2`

**Purpose**: Allows users to upload an invoice as an XML file.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `File bytes`: The XML invoice file to be uploaded.

- **Response**:
```json
{
  "invoice_id": 123456  // Unique identifier for the uploaded invoice.
}
```

- **Errors**:
  - 400: 
    - The file does not end in `.xml`.
    - The filename is longer than 100 characters.
  - 402: Invalid token.

---

### **POST** `/invoice_processing/upload_text/v2`

**Purpose**: Allows users to upload an invoice in plain text format.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice` (string): The plain text of the invoice.

- **Response**:
```json
{
  "invoice_id": 123456  // Unique identifier for the uploaded invoice.
}
```

- **Errors**:
  - 400: Name of the invoice is longer than 100 characters.
  - 402: Invalid token.

---

### **POST** `/invoice_processing/lint/v2`

**Purpose**: Returns validation linting diagnostics for a given invoice.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice_id` (integer): ID of the invoice to lint.
  - `new_invoice` (string, optional): Updated invoice text to validate. If valid, the original invoice will be updated.

- **Response**:
```json
{
  "diagnostics": {...}  // Detailed diagnostics of linting/validation.
}
```

- **Errors**:
  - 400: `invoice_id` is less than 1.
  - 402: 
    - Invalid token.
    - Authenticated user did not originally upload the invoice.

---

### **GET** `/invoice_processing/get/v2`

**Purpose**: Fetches information about a specific invoice.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice_id` (integer): ID of the invoice to retrieve.
  - `verbose` (boolean, optional): If true, returns extended invoice data.

- **Response**:
```json
{
  "invoice_data": {...} or
  "extended_invoice_data": {...}  // Depending on the verbose parameter.
}
```

- **Errors**:
  - 400: `invoice_id` is less than 1.
  - 402: Invalid token.

---

### **GET** `/invoice_processing/list_all/v2`

**Purpose**: Lists all invoices associated with the authenticated user.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `is_valid` (boolean, optional): If provided, returns only valid or invalid invoices based on its value.
  - `verbose` (boolean, optional): If true, returns extended invoice data.

- **Response**:
```json
{
  "invoice_datas": [...]
}
```
or 
```json
{
  "extended_invoice_datas": [...]
}
```

- **Errors**:
  - 402: Invalid token.

---

### **DELETE** `/invoice_processing/delete/v2`

**Purpose**: Deletes a specific invoice and all its associated data.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `invoice_id` (integer): ID of the invoice to delete.

- **Response**:
```json
{}  // Empty response indicating successful deletion.
```

- **Errors**:
  - 400: `invoice_id` is less than 1.
  - 402: Invalid token.

---

### **GET** `/invoice_processing/query/v2`

**Purpose**: Fetches processed/aggregated data from the database based on a query within a specified date range.

- **Parameters**:
  - `token` (string): User's authentication token.
  - `query` (string): Query to search the database.
  - `from_date` (date string): Start date in the format "YYYY-MM-DD".
  - `to_date` (date string): End date in the format "YYYY-MM-DD".

- **Response**:
```json
{
  "results": [...]
}
```

- **Errors**:
  - 400:
    - Invalid query.
    - Dates are not in the correct format.
  - 402: Invalid token.

---

## **Admin Operations**

Admin operations are typically privileged endpoints that are accessible only to users with elevated permissions. They can be used to manage resources, oversee user activity, and maintain the overall health of the application.

---

### **DELETE** `/clear/v1`

**Purpose**: Clears the entire database. This operation is a hard reset, and all data will be permanently erased.

- **Parameters**:
  - `token` (string): User's authentication token, which should belong to an admin or superuser.

- **Response**:
```json
{}  // Empty response indicating successful deletion.
```

- **Errors**:
  - 400: The operation is forbidden as the user is not recognized as the superuser.
  - 402: Invalid token.

**Caution**: Given the potentially destructive nature of this endpoint, it's essential to handle it with care.

---

This document provides a structured and user-friendly guide to interact with the ChurroFlow API. Refer to this document to understand the required parameters and potential errors for each API call.
