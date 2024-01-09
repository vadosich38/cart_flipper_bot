import logging
from DBPackage.DBclass import DBMethods

# Create DB\Tables if not
DBMethods.create_tables()

# Initialize system logger
logger = logging.getLogger('SYSTEM')
logging.basicConfig(level=logging.INFO,
                    filename='log.log',
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%H:%M:%S')
