from clickhouse_connect import get_client

client = get_client(host='localhost', username='default', password='')


def query_clickhouse(sql):
    result = client.query(sql)
    return result.result_rows
