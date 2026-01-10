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