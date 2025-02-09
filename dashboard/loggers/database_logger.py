import logging
from datetime import datetime
import os
from functools import wraps
import traceback
from pathlib import Path
class DatabaseLogger:
    def __init__(self, log_directory=None):
        # Create logs directory if it doesn't exist
        if log_directory is None:
            # Get the project root directory (where main.py is)
            project_root = Path(__file__).parent.parent.parent
            log_directory = project_root / 'logs'

        # Convert to Path object and create directories
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        (self.log_directory / 'errors').mkdir(exist_ok=True)
        (self.log_directory / 'info').mkdir(exist_ok=True)

        # Create logger
        self.logger = logging.getLogger('DatabaseLogger')
        self.logger.setLevel(logging.INFO)

        # Clear any existing handlers
        self.logger.handlers = []
        
        # Initialize context
        self.current_context = {}

        # Set up handlers
        self._setup_info_handler()
        self._setup_error_handler()
        self._setup_console_handler()


    def _setup_console_handler(self):
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d - %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def set_context(self, **kwargs):
        """Set context information for logging"""
        self.current_context.update(kwargs)
        
    def clear_context(self):
        """Clear the current context"""
        self.current_context = {}
        
    def _format_context(self):
        """Format the current context for logging"""
        if not self.current_context:
            return ""
        return " | " + " | ".join(f"{k}: {v}" for k, v in self.current_context.items())
        
    def _setup_info_handler(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(
            self.log_directory / 'info' / f'db_operations_{current_date}.log'
        )
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        file_handler.addFilter(lambda record: record.levelno == logging.INFO)
        self.logger.addHandler(file_handler)
    def _setup_error_handler(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        error_handler = logging.FileHandler(
            self.log_directory / 'errors' / f'db_errors_{current_date}.log'
        )
        error_handler.setLevel(logging.ERROR)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
            'Additional Details:\n'
            '%(pathname)s:%(lineno)d\n'
        )
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    # Add these proxy methods
    def error(self, message):
        self.logger.error(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
    @staticmethod
    def log_db_operation(operation_name):
        """Decorator for logging database operations"""
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # Get logger directly from self since we know it exists
                
                context = self._format_context() if hasattr(self, '_format_context') else ""
                
                try:
                    self.logger.info(f"Starting {operation_name}{context}")
                    result = func(self, *args, **kwargs)
                    self.logger.info(f"Successfully completed {operation_name}{context}")
                    return result
                except Exception as e:
                    self.logger.error(
                        f"Error in {operation_name}{context}: {str(e)}\n"
                        f"Traceback: {traceback.format_exc()}"
                    )
                    raise
            return wrapper
        return decorator
   