# src/patients/utils/encryption.py
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

def encrypt(txt):
    try:
        # Convert integer, etc., to string first
        txt = str(txt)
        # Get the key from settings (it should be in bytes)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)  
        # Input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('utf-8'))
        # Encode to URL-safe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("utf-8")
        return encrypted_text
    except Exception as e:
        # Log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

def decrypt(txt):
    try:
        # Base64 decode
        txt = base64.urlsafe_b64decode(txt.encode("utf-8"))
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("utf-8")
        return decoded_text
    except Exception as e:
        # Log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None