# helper function to compile program source
import base64

from config.algod_client import algod_client


def compile_program(source_code):
    """
    Used to compile the program into binary
    :param source_code: TEAL code
    :return: encoded program
    """
    compile_response = algod_client.compile(source_code)
    return base64.b64decode(compile_response['result'])


def compile_smart_signature(source_code):
    """
        Used to compile the SMART SIGNATURE into binary, different as this is for stateless contracts
    :param source_code: TEAL code
    :return: encoded program
    """
    compile_response = algod_client.compile(source_code)
    return compile_response['result'], compile_response['hash']
