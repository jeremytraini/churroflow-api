from typing import Dict


def health_check_v1() -> Dict:
    '''
    Checks that the server is functioning properly.

    Arguments:
        None

    Exceptions:
        None

    Return Value:
        is_alive: True if the server is alive, False otherwise
    '''
    
    return {'is_alive': True}
