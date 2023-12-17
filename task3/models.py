import clickhouse_connect
import pandas as pd


def create_table(database='antonovao', table='move_mouse'):
    client = clickhouse_connect.get_client(host='localhost', username='default')
    client.command(f'''CREATE TABLE if not exists {database}.{table} (
        x Int16, 
        y Int16, 
        deltaX Int16, 
        deltaY Int16, 
        clientTimeStamp DateTime, 
        button Int8, 
        target String
    ) ENGINE = MergeTree()  
    order by clientTimeStamp''')

    client.command(f'''CREATE TABLE if not exists {database}.{table}_buffer (
        x Int16, 
        y Int16, 
        deltaX Int16, 
        deltaY Int16, 
        clientTimeStamp DateTime, 
        button Int8, 
        target String
    ) ENGINE = Buffer ({database}, {table}, 16, 10, 100, 10000, 1000000, 10000000, 100000000)''')


def insert_data(data, database='antonovao', table='move_mouse'):
    client = clickhouse_connect.get_client(host='localhost', username='default')
    client.insert(f'{database}.{table}_buffer', [data])


def select_data(query):
    client = clickhouse_connect.get_client(host='localhost', username='default')
    answer = client.query(query)
    return pd.DataFrame(answer.result_set, columns=answer.column_names)

def drop_table(database='antonovao', table='move_mouse'):
    client = clickhouse_connect.get_client(host='localhost', username='default')
    client.command(f'DROP TABLE IF EXISTS {database}{table}')
