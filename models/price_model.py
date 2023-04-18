import pandas as pd
import numpy as np

def get_price_info(conn):
    return pd.read_sql('''
        SELECT id_type,type_name AS Тип_Велосипеда, price_type AS Цена_День, pledge AS Залог FROM TypeBicycle;
    ''',conn)

def get_selected_type(conn,id_type):
    return pd.read_sql('''
        SELECT id_type,type_name AS Тип_Велосипеда, price_type AS Цена_День, pledge AS Залог FROM TypeBicycle
        WHERE id_type =:id_type;
    ''',conn,params={"id_type":id_type})

def update_type_price(conn,id_type,price_type,pledge):
    cur = conn.cursor()
    cur.execute('''
        UPDATE TypeBicycle SET price_type=:price_type, pledge=:pledge
        WHERE id_type=:id_type
        ''', {"id_type": id_type, "price_type": price_type, "pledge":pledge})
    conn.commit()
    return True