import json
import mysql.connector
import logging

logger = logging.getLogger('flashscore')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

HOST = config['HOST']
USER = config['USER']
PASSWORD = config['PASSWORD']
DATABASE = config['DATABASE']
SQL_FILE_PATH = config['SQL_FILE_PATH']

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    auth_plugin='caching_sha2_password'
)

cursor = connection.cursor()


def create_db():
    """
    Runs the flash.sql file in order to create and set the flashscore Database.
    It connects to mysql through the variables given on the DMconf.json file:
    host=HOST
    user=USER
    password=PASSWORD
    """
    try:
        if connection.is_connected():
            with open(SQL_FILE_PATH, 'r') as sql_file:
                sql_statements = sql_file.read()

            queries = sql_statements.split(';')

            create_db_query = "CREATE DATABASE IF NOT EXISTS `{}`;"
            use_db_query = 'USE `{}`;'

            cursor.execute(create_db_query.format(DATABASE))
            cursor.execute(use_db_query.format(DATABASE))

            for query in queries:
                if query.strip():
                    cursor.execute(query)

            connection.commit()
            logger.info("SQL file executed successfully")
            cursor.close()

    except mysql.connector.Error as e:
        logger.error(f"SQL file not executed: {e}")
        print(f'Error: {e}')

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed.')
