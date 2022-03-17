import pandas.io.sql
import pyodbc
from dms_db_connection import dms_sql_connection
import pandas as pd
from dms_init_logger import log

logger = log('DMS DB QUERY MONITORING INGESTION')

query_parent_message_id = 'SELECT TOP (1) PARENT_MESSAGEID FROM CRTD.CRTD_STATUS ORDER BY CREATED_DATETIME DESC;'
query_message_id = 'SELECT PARENT_MESSAGEID,MESSAGEID,STATUS,FINAL_STATUS,CREATED_DATETIME,MODIFIED_DATETIME ' \
                   'FROM CRTD.CRTD_STATUS WHERE PARENT_MESSAGEID IN (?);'
query_error = 'SELECT * FROM ERROR.ERROR  WHERE MessageID IN (?);'
query_receiver_entity_map = 'SELECT * FROM CRTD.CRTD_RECEIVER_ENTITY_MAP;'


def dms_status_table_parent_message_id():
    connection = dms_sql_connection()
    try:
        logger.info('Executing query... DMS Parent message ID')
        parent_message_id = pd.read_sql_query(query_parent_message_id, con=connection)
        return parent_message_id
    except pyodbc.Error as ex:
        logger.log('ERROR QUERY PARENT ID')
        logger.error(ex)


def dms_status_table_message_id():
    connection = dms_sql_connection()
    try:
        list_parent_message_id = dms_status_table_parent_message_id()
        list_parent_message_id = list_parent_message_id['PARENT_MESSAGEID'].tolist()
        message_id = pd.read_sql_query(query_message_id, params=list_parent_message_id, con=connection)
    except pyodbc.Error as ex:
        logger.log('ERROR QUERY MESSAGE ID')
        logger.error(ex)
    return message_id


def dms_error_table():
    connection = dms_sql_connection()
    try:
        list_message_id = dms_status_table_message_id()
        list_message_id = list_message_id['MESSAGEID'].tolist()
        error = pd.read_sql_query(query_error, params=list_message_id, con=connection)
    except pyodbc.Error as ex:
        logger.log('ERROR QUERY -ERROR TABLE- !')
        logger.error(ex)
    return error


def dms_error_table_file_name(file_name="", error_type="", date="", column=""):
    error = pd.DataFrame({'Message': ['No data to display']})
    error_type_value = error_type
    date_value = date
    column_value = column
    if error_type != '':
        error_type = 'AND errorDesc  {0}'.format(error_type_value)
    if date != '':
        date = 'AND ErrorDate {0}'.format(date_value)
    if column != '':
        column = 'AND columnName {0}'.format(column_value)

    query_error_file_name = 'SELECT E.ColumnName,E.ErrorDesc, E.ErrorUIDs,action ' \
                            'FROM CRTD.CRTD_STATUS AS CS JOIN ERROR.ERROR AS E  ' \
                            'ON CS.MESSAGEID = E.MessageID {0} {1} {2}' \
                            'WHERE CS.FILE_NAME = ?; '.format(date, column, error_type)
    connection = dms_sql_connection()
    file_name = [file_name]

    try:
        error = pd.read_sql_query(query_error_file_name, params=file_name, con=connection)
        logger.info(' "Error Status Query" Execution Finished .....')
        logger.info(query_error_file_name)
    except pandas.io.sql.DatabaseError as e:
        logger.info('Query Error!!')
        logger.info('Verify your query!!!')
        logger.info(query_error_file_name)
        logger.error(e)
    return error

def dms_receiver_entity_map():
    connection = dms_sql_connection()
    try:
        logger.info('Executing query... DMS receiver_entity_map')
        receiver_entity_map = pd.read_sql_query(query_receiver_entity_map, con=connection)
        return receiver_entity_map
    except pyodbc.Error as ex:
        logger.log('ERROR QUERY RECEIVER ENTITY MAP')
        logger.error(ex)