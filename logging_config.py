def generate_secure_password(length=16):
    """Generate a random secure password using the secrets module.
    Returns a string of `length` characters containing letters, digits, and punctuation.
    """
    import secrets, string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
import logging
import os
from datetime import datetime

def setup_logger(name: str = None, log_file: str = None) -> logging.Logger:
    """Configure logging for security testing tool"""
    if log_file is None:
        os.makedirs('logs', exist_ok=True)
        log_file = f'logs/security_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
    
    return logger
# Updated on 2026-11-12


# Updated on 2026-11-12
