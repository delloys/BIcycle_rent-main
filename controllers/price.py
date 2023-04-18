from app import app
from flask import render_template, request

from models.price_model import *
from utils import get_db_connection

@app.route('/price', methods=['get', 'post'])

def price():

    conn = get_db_connection()

    if request.values.get('id_type'):
        id_type=(request.values.get('id_type'))
    else:
        id_type=-1

    if request.values.get('id_type_changed'):
        id_type = request.values.get("id_type_changed")
        price_type = request.values.get("price_type")
        pledge = request.values.get("pledge")
        update_type_price(conn,id_type,price_type,pledge)

    df_get_price_info = get_price_info(conn)
    df_get_selected_type = get_selected_type(conn,id_type)

    html = render_template(
        'price.html',
        get_price_info = df_get_price_info,
        get_selected_type = df_get_selected_type,
        len = len
    )
    return html