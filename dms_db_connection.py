import pyodbc
from dms_env_config import config_file
from dms_init_logger import log

logger = log('DMS DB CONNECTION')


def dms_sql_connection() -> object:  # Return DB Connection
    env = config_file()
    sql_server = env['sql_dms_db'][0]['sql_dms_server']
    sql_username = env['sql_dms_db'][0]['sql_dms_username']
    sql_password = env['sql_dms_db'][0]['sql_dms_password']
    sql_db = env['sql_dms_db'][0]['sql_dms_database']
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql_server + ';DATABASE=' + sql_db +
            ';UID=' + sql_username + ';PWD=' + sql_password)
        logger.info('Successfully connection DMS DB !')
        return connection
    except pyodbc.Error as ex:
        logger.error(ex)
