import mysql.connector

# Set your MySQL connection parameters
HOST = DMconf['HOST']
USER = DMconf['USER']
PASWORD = DMconf['PASWORD']
DATABASE = DMconf['DATABASE']  # Assuming your database is named 'flashscore'

sql_file_path = 'flash.sql'

try:
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASWORD
    )

    if connection.is_connected():
        print(f'Connected to MySQL database: {database}')

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Read and execute SQL statements from the file
        with open(sql_file_path, 'r') as sql_file:
            sql_statements = sql_file.read()

        # Split SQL statements into individual queries
        queries = sql_statements.split(';')

        # Execute each query one by one
        for query in queries:
            if query.strip():
                cursor.execute(query)

        # Commit the changes
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
