from app import app
from flask import render_template, request
from utils import get_db_connection
from models.model_addbicycle import *

@app.route('/addbicycle', methods=['get', 'post'])

def addbicycle():

    conn = get_db_connection()
    df_model_names = get_bike_model(conn)

    html = render_template(
        'addbicycle.html',
        model_names = df_model_names,
        len=len
    )
    return html