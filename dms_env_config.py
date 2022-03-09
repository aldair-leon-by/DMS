import json
from dms_init_logger import log
from dms_abs_path import path_resources_folder
from os import path

logger = log('ENV_CONFIG')


def config_file() -> object:  # Return DMS DB credentials
    path_config_file = path_resources_folder()  # get abs path for resource file
    if path.exists(path_config_file):
        with open(path_config_file) as f:
            sql_connection = json.load(f)
        logger.info('SUCCESSFUL LOAD CONFIG FILE')
        return sql_connection  # Return json DB Credentials
    else:
        logger.info('ERROR PATH DOESNT EXIST !')  # Logger error
