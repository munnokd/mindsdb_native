import pandas as pd
from pymongo import MongoClient

from mindsdb_native.libs.data_types.data_source import DataSource


class MongoDS(DataSource):

    def _setup(self, query=None, table, host='localhost', port=27017,
               user='postgres', password='', database='postgres'):

        if query is None:
            query = f'SELECT * FROM {table}'

        conn = MongoClient(host=host, post=port, username=user,
                           password=password, authSource=database,
                           authMechanism='SCRAM-SHA-256')
        
        db = conn[database]
        cursor = db[collection].find(query)

        df = pd.DataFrame(list(cursor))

        df.columns = [x.decode('utf-8') for x in df.columns]
        for col_name in df.columns:
            try:
                df[col_name] = df[col_name].apply(lambda x: x.decode("utf-8"))
            except:
                pass

        col_map = {}
        for col in df.columns:
            col_map[col] = col

        return df, col_map


if __name__ == '__main__':
