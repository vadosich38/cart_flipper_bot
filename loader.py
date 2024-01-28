import logging



print('Инициализация логгера')
# Initialize system logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger('SYSTEM')

