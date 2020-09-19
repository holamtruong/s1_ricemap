'''
Some functions to CRUD Postgres database by Truong Ho
'''

import psycopg2
from postgres4Py import pgDBConfig


# Check PostgreSQL database version
def check_db_version():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = pgDBConfig.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# Select all rows of a table
def select_all_row(schema, table):
    conn = None
    try:
        # read connection parameters
        params = pgDBConfig.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # create a SQL command
        sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
        print(sql_command)

        # execute a statement
        cur.execute(sql_command)
        records = cur.fetchall()
        conn.close()
        return records

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# Select all rows of a table
def select_row_where(schema, table, select_col, select_value):
    conn = None
    try:
        # read connection parameters
        params = pgDBConfig.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql_command = "SELECT * FROM {}.{} WHERE {} = {};".format(str(schema), str(table), str(select_col),
                                                                  str(select_value))
        print(sql_command)

        # execute a statement
        cur.execute(sql_command)

        records = cur.fetchall()
        conn.close()
        return records

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# insert into multi column
def insert_multi_column(schema, table, list_col, list_value):
    conn = None
    try:
        # read connection parameters
        params = pgDBConfig.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # get list of columns, values
        fieldList = str()
        valueList = str()
        for field in list_col:
            fieldList = fieldList + ", " + field
        for value in list_value:
            valueList = valueList + ", \'" + str(value) + "\'"
        # create a SQL command
        sql_command = '''INSERT INTO {}.{} ({}) VALUES ({});'''.format(str(schema), str(table),
                                                                       str(fieldList[1:]), str(valueList[1:]))
        print(sql_command)

        # execute a statement
        cur.execute(sql_command)

        # commit the changes to the database
        conn.commit()

        # count successfully result
        print(cur.rowcount, "Record inserted successfully into the table.")
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# insert into multi column with list key-value
def insert_multi_column_keyvalue(schema, table, list_col, list_value):
    conn = None
    try:
        # read connection parameters
        params = pgDBConfig.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # get list of columns, values
        fieldList = str()
        valueList = str()
        for field in list_col:
            fieldList = fieldList + ", " + field
        for value in list_value:
            valueList = valueList + ", \'" + str(value) + "\'"
        # create a SQL command
        sql_command = '''INSERT INTO {}.{} ({}) VALUES ({});'''.format(str(schema), str(table),
                                                                       str(fieldList[1:]), str(valueList[1:]))
        print(sql_command)

        # execute a statement
        cur.execute(sql_command)

        # commit the changes to the database
        conn.commit()

        # count successfully result
        print(cur.rowcount, "Record inserted successfully into the table.")
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':





    '''
    list_col = ['name', 'properties', 'weight', 'birthday']
    list_val = ['a small dog', 'Bad dog', 4.543113, '2017-01-21']
    insert_multi_column('public', 'lusuno', list_col, list_val)
    '''

    '''
    rs = select_all_row('public', 'lusuno')
    print(rs)
    '''

    '''
    rs = select_row_where('public', 'lusuno', 'id', 1)
    print(rs)
    '''
