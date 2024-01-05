import logging

logger = logging.getLogger('SYSTEM')
logging.basicConfig(level=logging.INFO,
                    filename='log.log',
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%H:%M:%S')