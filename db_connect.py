import mysql.connector

host = 'localhost'
user = 'root'
password = '******'  # insert local password
sql_file_path = 'flash.sql'

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

cursor = connection.cursor()

try:
    if connection.is_connected():

        with open(sql_file_path, 'r') as sql_file:
            sql_statements = sql_file.read()

        # Split SQL statements into individual queries
        queries = sql_statements.split(';')

        # Execute each query one by one
        for query in queries:
            if query.strip():
                cursor.execute(query)

        connection.commit()

        print('SQL file executed successfully.')

        # Close the cursor and connection
        cursor.close()

except mysql.connector.Error as e:
    print(f'Error: {e}')

finally:
    if connection.is_connected():
        connection.close()
        print('MySQL connection closed.')
