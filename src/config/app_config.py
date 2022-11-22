import os
import logging
from dotenv import load_dotenv

load_dotenv()

# FETCH ENVIRONMENT VARIABLES
SECRET_KEY = os.getenv("SECRET_KEY")

# CONFIGURE LOGGER
logger = logging.getLogger("c360_encryption_python")
log_formatter = logging.Formatter('%(asctime)s->%(levelname)s in %(module)s: %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)