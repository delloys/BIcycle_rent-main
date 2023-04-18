import pandas as pd
import numpy as np

def get_bike_model(conn):
    return pd.read_sql('''
        SELECT id_model, name_model FROM ModelBicycle;
    ''',conn)

