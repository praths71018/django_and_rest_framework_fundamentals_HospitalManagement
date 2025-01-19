import logging
import os

# Set up logging configuration
log_file_path = os.path.join('logs', 'app.log')  # Ensure the 'logs' directory exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    # This is called when the request is received
    def __call__(self, request, *args, **kwargs):
        # Log the URL being accessed
        self.logger.info(f'Entered URL: {request.path}')
        
        response = self.get_response(request)
        
        return response
