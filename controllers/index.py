from app import app
from flask import render_template, request, session
from utils import get_db_connection
import pandas as pd
from datetime import datetime
from models.index_model import *

@app.route('/', methods=['get', 'post'])
def index():

    conn = get_db_connection()

    current_date = datetime.now().date()
    count_plus = 0
    list_dmg = []
    list_num = []
    list_dmg1 = []
    list_num1 = []
    itogo_dmg = 0
    itogo = 0
    df_table = pd.DataFrame([
                       [1, 'В наличии', 'get_tabl3'],
                       [2, 'Отсутствуют', 'get_tabl5']],
                      columns=['id', 'name', 'text'])

    if request.values.get('id_bike'):
        id_bike=(request.values.get('id_bike'))
    else:
        id_bike=-1

    if request.values.get('return_bike') and request.values.get('damage0'):
        for i in range(count_plus+1):
            list_dmg1.append(request.values.get('damage' + str(i)))
            list_num1.append(request.values.get('num' + str(i)))
        if len(list_dmg1) !=0:
            for i in range(len(list_dmg1)):
                df_type_dmg = get_dmg_type(conn, list_dmg1[i])
                df_get_dmg = get_dmg_rented(conn, request.values.get('id_bike_return'), request.values.get('date_return'), request.values.get('idbike_rental'), list_num1[i], df_type_dmg.loc[0,'damage_name'], list_dmg1[i])
    elif request.values.get('return_bike') and not request.values.get('damage0'):
        get_rented(conn, request.values.get('id_bike_return'), request.values.get('date_return'))

    if request.values.get('id_to_repair'):
        bike_to_repair(conn,request.values.get('id_to_repair'))

    if request.values.get('id_bike_from_repair'):
        bike_from_repair(conn, request.values.get('id_bike_from_repair'))

    if request.values.get('id_to_kill'):
        bike_to_kill(conn,request.values.get('id_to_kill'))

    if request.values.get('id_bike_return'):
        id_bike=(request.values.get('id_bike_return'))

    if request.form.get('clear'):
        models=[]
        brands=[]
        types=[]
        years=[]
        table='get_tabl4'
    elif request.values.get('id_bike_rent'):
        models = request.form.getlist('Модель')
        brands = request.form.getlist('Бренд')
        types = request.form.getlist('Тип')
        years = request.form.getlist('Год_Выпуска')
        table = request.form.get('Наличие')
        for i in range(len(years)):
            years[i] = int(years[i])
        to_rent(conn, request.values.get('date_issue'),request.values.get('id_bike_rent'),request.values.get('client'))
    elif request.values.get('id_bike_return'):
        models = request.form.getlist('Модель')
        brands = request.form.getlist('Бренд')
        types = request.form.getlist('Тип')
        years = request.form.getlist('Год_Выпуска')
        table = request.form.get('Наличие')
        for i in range(len(years)):
            years[i] = int(years[i])
        for i in range(count_plus):
            list_dmg1.append(request.values.get('damage' + str(i)))
            list_num1.append(request.values.get('num' + str(i)))
        for i in range(len(list_dmg1)):
            df_type_dmg = get_dmg_type(conn, list_dmg1[i])
        #get_rented(conn,request.values.get('id_bike_return'),request.values.get('date_return'))
    else:
        models=request.form.getlist('Модель')
        brands=request.form.getlist('Бренд')
        types=request.form.getlist('Тип')
        years=request.form.getlist('Год_Выпуска')
        table = request.form.get('Наличие')
        for i in range(len(years)):
            years[i] = int(years[i])

    if request.values.get('idbike_rental'):
        get_bicycle_rental = request.values.get('idbike_rental')
    if request.values.get('date_issue_add'):
        add_bicycle(conn,request.values.get('date_issue_add'),request.values.get('model_name_add'))

    df_date_issue = get_date_i(conn, id_bike)
    if request.values.get('confirm'):
        count_plus = int(request.values.get('count_dmg'))
        for i in range(count_plus + 1):
            list_dmg.append(request.values.get('damage' + str(i)))
            list_num.append(request.values.get('num' + str(i)))
        if request.values.get('date_return'):
            ret = datetime.strptime(request.values.get('date_return'), '%Y-%m-%d')
            iss = datetime.strptime(df_date_issue.loc[0, 'date_issue'], '%Y-%m-%d')
            dayS = (ret - iss).days

            pay_for_day = request.values.get('pay_check')
            for i in range(len(list_num)):
                if list_num[i]!='':
                    list_num[i] = int(list_num[i])
                    itogo_dmg = itogo_dmg + list_num[i]
                else:
                    break
            itogo = dayS * int(pay_for_day) + itogo_dmg
    elif request.values.get('count_dmg'):
        count_plus = int(request.values.get('count_dmg')) + 1 + count_plus
        for i in range(count_plus):
            list_dmg.append(request.values.get('damage' + str(i)))
            list_num.append(request.values.get('num' + str(i)))

    if request.values.get('id_bike_view_dmg'):
        view_dmg_id = request.values.get('id_bike_view_dmg')
        df_one_day_price = get_one_day_price(conn, view_dmg_id)
    else:
        view_dmg_id = -1
        df_one_day_price = get_one_day_price(conn, id_bike)

    df_pledge = get_pledge(conn, id_bike)
    df_pay_day = get_pay_day(conn, id_bike)
    df_damage = get_damage(conn)
    df_one_bike = get_one_bike(conn, id_bike)
    df_dmg_bike = get_dmg_for_bike(conn)
    df_get_one_dmg = get_one_dmg(conn,id_bike)
    df_get_all_dmg_price = get_all_dmg_price(conn,id_bike)
    df_dmg = df_dmg_bike['id_bike'].tolist()
    df_bicycle_rental = get_bike_rental(conn, id_bike)
    df_info = get_info(conn, id_bike)
    df_client = get_client(conn)
    df_bicycle_list = get_bicycle_list(conn, models, brands, types, years, table)
    df_type = get_type(conn)
    df_brand = get_brand(conn)
    df_model = get_model(conn)
    df_year = get_year(conn)
    df_rent_bike = get_rent_bike(conn)
    df = df_rent_bike['id_b'].tolist()
    date_return = request.values.get('date_return')

    for index, row in df_pay_day.iterrows():
        if (4 >= int(current_date.year)-int(row['Год_Выпуска']) > 3):
            df_pay_day['price_type'][index]= row['price_type'] * 0.9
        elif (5>=int(current_date.year)-int(row['Год_Выпуска']) > 4):
            df_pay_day['price_type'][index] = row['price_type'] * 0.8
        elif (int(current_date.year)-int(row['Год_Выпуска']) > 5):
            df_pay_day['price_type'][index] = row['price_type'] * 0.7

    for index, row in df_bicycle_list.iterrows():
        if (4 >= int(current_date.year)-int(row['Год_Выпуска']) > 3):
            df_bicycle_list['Цена_День'][index]= row['Цена_День'] * 0.9
        elif (5>=int(current_date.year)-int(row['Год_Выпуска']) > 4):
            df_bicycle_list['Цена_День'][index] = row['Цена_День'] * 0.8
        elif (int(current_date.year)-int(row['Год_Выпуска']) > 5):
            df_bicycle_list['Цена_День'][index] = row['Цена_День'] * 0.7
    for index, row in df_one_bike.iterrows():
        if (4 >= int(current_date.year)-int(row['Год_Выпуска']) > 3):
            df_one_bike['Цена_День'][index]= row['Цена_День'] * 0.9
        elif (5>=int(current_date.year)-int(row['Год_Выпуска']) > 4):
            df_one_bike['Цена_День'][index] = row['Цена_День'] * 0.8
        elif (int(current_date.year)-int(row['Год_Выпуска']) > 5):
            df_one_bike['Цена_День'][index] = row['Цена_День'] * 0.7

    html = render_template(
        'index.html',
    bicycle_list = df_bicycle_list,
    list_df = [df_type, df_brand, df_model, df_year,df_table],
    sections = ['Тип','Бренд','Модель','Год_Выпуска','Наличие'],
    list_choices = [types, brands, models, years, table],
    rent_bike = df,
    info = df_info,
    client = df_client,
    id_bike = id_bike,
    damage = df_damage,
    count_plus = count_plus,
    get_bike = df_one_bike,
    list_dmg = list_dmg,
    list_num = list_num,
    clien = df_client,
    dmg_for_bike = df_dmg_bike,
    dmg_check = df_dmg,
    get_one_dmg = df_get_one_dmg,
    df_bicycle_rental = df_bicycle_rental,
    date_ret = date_return,
    date_issue = df_date_issue,
    pay_day = df_pay_day,
    pledge = df_pledge,
    itogo = itogo,
    view_dmg_id = view_dmg_id,
    get_all_dmg_price = df_get_all_dmg_price,
    one_day_price = df_one_day_price,
    len=len,
    str = str,
    zip = zip)
    return html