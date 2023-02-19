from datetime import datetime 
import uuid 
import logging
import os
import yaml
from attrdict import AttrDict

def load_config(config_dir):
    with open(config_dir, 'rb') as f :
        config = yaml.load(f, Loader=yaml.FullLoader)
    args = AttrDict(config)
    return args

def generate_serial_number():
    return datetime.today().strftime('%Y-%m-%d') + '-' + str(uuid.uuid1()).split('-')[0]


def get_logger(name: str, dir_: str, stream=False) -> logging.RootLogger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO) # logging all levels
    
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(os.path.join(dir_, f'{name}.log'))

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if stream:
        logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    return logger