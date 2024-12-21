import logging
import os
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class CustomLogger:
    def __init__(self, name, log_file=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Create console handler with coloring
        console_handler = ColoredConsoleHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create file handler if log_file is provided
        if log_file:
            log_file = os.path.join('logs', log_file)
            self._setup_file_handler(log_file, formatter)

    def _setup_file_handler(self, log_file, formatter):
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)

    def log_exception(self, message):
        self.logger.exception(message)

    def log_api_request(self, method, path, status_code, response_time):
        self.logger.info(
            f"API Request - Method: {method}, Path: {path}, "
            f"Status: {status_code}, Response Time: {response_time:.2f}s"
        )

    def log_db_query(self, query, execution_time):
        self.logger.debug(
            f"Database Query - Query: {query}, "
            f"Execution Time: {execution_time:.2f}s"
        )

    def log_user_action(self, user_id, action):
        self.logger.info(f"User Action - User ID: {user_id}, Action: {action}")


class ColoredConsoleHandler(logging.StreamHandler):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def emit(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        message = self.format(record)
        print(f"{color}{message}{Style.RESET_ALL}")


# Usage example
# logger = CustomLogger("MyApp", log_file="logs/app.log")
# logger.log_info("This is an info message")
# logger.log_warning("This is a warning message")
# logger.log_error("This is an error message")
# logger.log_critical("This is a critical message")
# logger.log_api_request("GET", "/api/users", 200, 0.05)
# logger.log_db_query("SELECT * FROM users", 0.02)
# logger.log_user_action("user123", "Logged in")