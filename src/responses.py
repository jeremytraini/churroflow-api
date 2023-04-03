# Sample responses to be shown in FastAPI Swagger section

health_check = {
    200: {
        "description": "Server is up."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_upload_file_v1 = {
    200: {
        "description": "File is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_upload_file_v2 = {
    200: {
        "description": "File is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_bulk_upload_file_v1 = {
    200: {
        "description": "All files are successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_bulk_upload_file_v2 = {
    200: {
        "description": "All files are successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_upload_text_v1 = {
    200: {
        "description": "Text is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_upload_text_v2 = {
    200: {
        "description": "Text is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_bulk_upload_text_v1 = {
    200: {
        "description": "All text is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_bulk_upload_text_v2 = {
    200: {
        "description": "All text is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_upload_url_v1 = {
    200: {
        "description": "URL is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_invoice_upload_url_v2 = {
    200: {
        "description": "URL is successfully uploaded."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_json_report_v1 = {
    200: {
        "description": "JSON Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_json_report_v2 = {
    200: {
        "description": "JSON Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    403: {
        "description": "User does not have permission to perform this action."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_bulk_json_report_v1 = {
    200: {
        "description": "All JSON Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_bulk_json_report_v2 = {
    200: {
        "description": "All JSON Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    403: {
        "description": "User does not have permission to perform this action."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_pdf_report_v1 = {
    200: {
        "description": "PDF Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_pdf_report_v2 = {
    200: {
        "description": "PDF Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    403: {
        "description": "User does not have permission to perform this action."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_bulk_pdf_report_v1 = {
    200: {
        "description": "All PDF Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_bulk_pdf_report_v2 = {
    200: {
        "description": "All PDF Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    403: {
        "description": "User does not have permission to perform this action."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_html_report_v1 = {
    200: {
        "description": "HTML Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_html_report_v2 = {
    200: {
        "description": "HTML Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    403: {
        "description": "User does not have permission to perform this action."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_csv_report_v1 = {
    200: {
        "description": "CSV Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_export_csv_report_v2 = {
    200: {
        "description": "CSV Report has been successfully exported."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    403: {
        "description": "User does not have permission to perform this action."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_wellformedness_v1 = {
    200: {
        "description": "Report has been successfully checked for wellformedness."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_schema_v1 = {
    200: {
        "description": "Report has been successfully checked for schema errors."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_syntax_v1 = {
    200: {
        "description": "Report has been successfully checked for syntax errors."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_peppol_v1 = {
    200: {
        "description": "Report has been successfully checked for PEPPOL errors."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_list_all_v1 = {
    200: {
        "description": "All reports are successfully listed."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_list_all_v2 = {
    200: {
        "description": "All reports are successfully listed."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_list_by_v1 = {
    200: {
        "description": "All reports are successfully listed by specified order."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_list_by_v2 = {
    200: {
        "description": "All reports are successfully listed by specified order."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_check_validity_v1 = {
    200: {
        "description": "Report has been checked for validity successfully."
    },
    400: {
        "description": "Input is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_lint_v1 = {
    200: {
        "description": "Report has been linted successfully."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_change_name_v2 = {
    200: {
        "description": "Report name has been successfully changed."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_report_delete_v2 = {
    200: {
        "description": "Report has been successfully deleted."
    },
    400: {
        "description": "Input is invalid."
    },
    401: {
        "description": "Token is invalid."
    },
    404: {
        "description": "Report id cannot be found."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_auth_login_v2 = {
    200: {
        "description": "User has logged in successfully."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}

res_auth_register_v2 = {
    200: {
        "description": "User has successfully registered."
    },
    400: {
        "description": "Input is invalid."
    },
    500: {
        "description": "An internal server error has occurred."
    }
}
