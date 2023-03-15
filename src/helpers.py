from tempfile import NamedTemporaryFile
from src.type_structure import *

def create_temp_file(invoice_text: str) -> str:
    tmp = NamedTemporaryFile(mode='w', delete=False)
    tmp.write(invoice_text)
    tmp.close()
    
    return tmp.name

def string_in_range(min_len:int, max_len:int, input_str:str) -> bool:
    '''
    This function checks if a string is within the ranges of min and max length.

    Arguments:
        min_len (int)   - Minimum length of string
        max_len (int)   - Maximum length of string
        input_str (str) - Input string to check length

    Return Value:
        Returns boolean to whether string is within range or not
    '''

    return len(input_str) >= min_len and len(input_str) <= max_len
