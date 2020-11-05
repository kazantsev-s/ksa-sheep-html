# -*- coding: UTF-8 -*-
from flask import Flask, render_template, url_for, app, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import xlrd, os, shutil, datetime
from datetime import datetime as dt, timedelta
from xlrd import open_workbook
from shutil import move
import psycopg2
from functools import wraps
from werkzeug.utils import secure_filename

db = create_engine('postgresql://postgres:123456@localhost:5432/postgres')
##db = create_engine('postgresql://postgres:Qwertyasdfsega161@localhost:5432/new1')

UPLOAD_FOLDER = 'xls_upload'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
defolt_limit = 50
defolt_limit = int(defolt_limit)
limit = defolt_limit
limit1 = defolt_limit
limit2 = defolt_limit
limit3 = defolt_limit
limit4 = defolt_limit

application = Flask(__name__)
application.secret_key = 'some secret secret'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SQLALCHEMY_DTABASE_URI'] = "posgresql://postgres:123456@localhost:5432/postgres"
##application.config['SQLALCHEMY_DTABASE_URI'] = "postgresql://postgres:Qwertyasdfsega161@localhost:5432/new1"


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('pie'))
        return f(*args, **kwargs)

    return inner


def login_required_user(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)

    return inner


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/day_stat', methods=['POST', 'GET'])
@login_required_user
def index():
    dateformat = '%Y-%m-%d'
    stat = db.execute("SELECT * from stat;")
    date_default = datetime.date.today()
    month_html = None
    month_html_y = None
    if request.method == "POST":
        datereport = request.form['dt_report']

        # работа с датой "сегодня"
        today_html = dt.strptime(datereport, dateformat)
        print(today_html)

        day_t = today_html.day
        day_t = str(day_t)

        month_t = today_html.month
        month_t = str(month_t)

        if day_t == '1' or day_t == '2' or day_t == '3' or day_t == '4' or day_t == '5' or day_t == '6' or day_t == '7' or day_t == '8' or day_t == '9':
            day_t = '0' + day_t

        if month_t == '1' or month_t == '2' or month_t == '3' or month_t == '4' or month_t == '5' or month_t == '6' or month_t == '7' or month_t == '8' or month_t == '9':
            month_t = '0' + month_t

        # опредление месяца
        if month_t == '01':
            month_html = '.01'
        elif month_t == '02':
            month_html = '.02'
        elif month_t == '03':
            month_html = '.03'
        elif month_t == '04':
            month_html = '.04'
        elif month_t == '05':
            month_html = '.05'
        elif month_t == '06':
            month_html = '.06'
        elif month_t == '07':
            month_html = '.07'
        elif month_t == '08':
            month_html = '.08'
        elif month_t == '09':
            month_html = '.09'
        elif month_t == '10':
            month_html = '.10'
        elif month_t == '11':
            month_html = '.11'
        elif month_t == '12':
            month_html = '.12'

        # работа с датой "вчера"
        yesterday_html = dt.strptime(datereport, dateformat) - timedelta(days=1)

        day_y = yesterday_html.day
        day_y = str(day_y)

        month_y = yesterday_html.month
        month_y = str(month_y)

        if day_y == '1' or day_y == '2' or day_y == '3' or day_y == '4' or day_y == '5' or day_y == '6' or day_y == '7' or day_y == '8' or day_y == '9':
            day_y = '0' + day_y

        if month_y == '1' or month_y == '2' or month_y == '3' or month_y == '4' or month_y == '5' or month_y == '6' or month_y == '7' or month_y == '8' or month_y == '9':
            month_y = '0' + month_y

        # опредление месяца
        if month_y == '01':
            month_html_y = '.01'
        elif month_y == '02':
            month_html_y = '.02'
        elif month_y == '03':
            month_html_y = '.03'
        elif month_y == '04':
            month_html_y = '.04'
        elif month_y == '05':
            month_html_y = '.05'
        elif month_y == '06':
            month_html_y = '.06'
        elif month_y == '07':
            month_html_y = '.07'
        elif month_y == '08':
            month_html_y = '.08'
        elif month_y == '09':
            month_html_y = '.09'
        elif month_y == '10':
            month_html_y = '.10'
        elif month_y == '11':
            month_html_y = '.11'
        elif month_y == '12':
            month_html_y = '.12'

        result_set = db.execute("select * from proc_one_day('" + datereport + "');")
        if result_set.rowcount < 1:
            messages_empty_rows = [" "]
            return render_template('index.html', date_default=date_default, stat=stat,
                                   messages_empty_rows=messages_empty_rows)
        return render_template('index.html', date_default=date_default, datereport=datereport, result_set=result_set,
                               stat=stat, month_html=month_html, month_html_y=month_html_y, day_t=day_t, day_y=day_y)
    return render_template('index.html', date_default=date_default, stat=stat)

    # datestart = "2000-01-01"
    # dateend = "2030-01-01"
    # result_set = db.execute("SELECT type, sum(count) as count FROM vw_stat where date(date_req) between date('" + datestart + "') and date('" + dateend + "') group by type order by count desc;")
    # return render_template('about.html', result_set=result_set)


# @login_required_user
@application.route('/')
@login_required_user
def pie():
    global baran_html, ovca_html, little_html, bolnoy_html, cnt_baran, cnt_ovca, cnt_little, cnt_bolnoy, cnt_old, old_html, stat_str
    stat_str = 0
    sql_script_baran_m = "SELECT type, count from vw_stat_index WHERE type = 'Баран' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'morning';"
    sql_script_ovca_m = "SELECT type, count from vw_stat_index WHERE type = 'Овца' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'morning';"
    sql_script_little_m = "SELECT type, count from vw_stat_index WHERE type = 'Ягненок' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'morning';"
    sql_script_bolnoy_m = "SELECT type, count from vw_stat_index WHERE type = 'Больной' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'morning';"
    sql_script_old_m = "SELECT type, count from vw_stat_index WHERE type = 'Старый' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'morning';"

    stat_str_e = 0
    sql_script_baran_e = "SELECT type, count from vw_stat_index WHERE type = 'Баран' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'evening';"
    sql_script_ovca_e = "SELECT type, count from vw_stat_index WHERE type = 'Овца' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'evening';"
    sql_script_little_e = "SELECT type, count from vw_stat_index WHERE type = 'Ягненок' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'evening';"
    sql_script_bolnoy_e = "SELECT type, count from vw_stat_index WHERE type = 'Больной' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'evening';"
    sql_script_old_e = "SELECT type, count from vw_stat_index WHERE type = 'Старый' and date_req = (SELECT max(date_req) from vw_stat) and time_of_day = 'evening';"

    def values_m(sql_script):
        values_sheep = db.execute(
            sql_script)
        if values_sheep.rowcount < 1:
            sheep_html = '0'
            cnt_sheep = 0
        else:
            for sheep in values_sheep:
                cnt = sheep.count
                cnt_sheep = cnt
                sheep_html = str(cnt)
                print(sheep_html)
        return sheep_html

    data_sql = db.execute("SELECT date_req from vw_stat_index WHERE date_req = (SELECT max(date_req) from vw_stat);")

    for i in data_sql:
        data_html = i.date_req
        data_html = str(data_html)
        data_html = data_html.replace('-', '.')
        break

    

    # morning_html

    baran_html = values_m(sql_script_baran_m)
    cnt_baran = int(baran_html)
    stat_str = stat_str + cnt_baran

    ovca_html = values_m(sql_script_ovca_m)
    cnt_ovca = int(ovca_html)
    stat_str = stat_str + cnt_ovca

    little_html = values_m(sql_script_little_m)
    cnt_little = int(little_html)
    stat_str = stat_str + cnt_little

    bolnoy_html = values_m(sql_script_bolnoy_m)
    cnt_bolnoy = int(bolnoy_html)
    stat_str = stat_str + cnt_bolnoy

    old_html = values_m(sql_script_old_m)
    cnt_old = int(old_html)
    stat_str = stat_str + cnt_old

    # evening_html

    baran_html_e = values_m(sql_script_baran_e)
    cnt_baran_e = int(baran_html_e)
    stat_str_e = stat_str_e + cnt_baran_e

    ovca_html_e = values_m(sql_script_ovca_e)
    cnt_ovca_e = int(ovca_html_e)
    stat_str_e = stat_str_e + cnt_ovca_e

    little_html_e = values_m(sql_script_little_e)
    cnt_little_e = int(little_html_e)
    stat_str_e = stat_str_e + cnt_little_e

    bolnoy_html_e = values_m(sql_script_bolnoy_e)
    cnt_bolnoy_e = int(bolnoy_html_e)
    stat_str_e = stat_str_e + cnt_bolnoy_e

    old_html_e = values_m(sql_script_old_e)
    cnt_old_e = int(old_html_e)
    stat_str_e = stat_str_e + cnt_old_e

    print('m' + str(stat_str))
    print('e' + str(stat_str_e))    # if 0 then e0

    if stat_str_e > 0:
        evening_html_check = True
    else:
        evening_html_check = False

    warning_messages = ['']
    check_pie = 11
    stat = db.execute("SELECT * from stat;")
    # for i in stat:
    #     stat_str = str(i.cnt)
    # print(stat_str)
    cnt_list_html = [int(baran_html), int(ovca_html), int(little_html), int(bolnoy_html), int(old_html)]
    cnt_list_html_e = [int(baran_html_e), int(ovca_html_e), int(little_html_e), int(bolnoy_html_e), int(old_html_e)]
    print(cnt_list_html)
    stat_str = str(stat_str)
    stat_int = int(stat_str)
    stat_int_e = stat_str_e
    stat_str_html_e = str(stat_str_e)
    print(stat_str)
    return render_template('pie.html', check_pie=check_pie, stat=stat, stat_str=stat_str, baran_html=baran_html,
                           ovca_html=ovca_html, little_html=little_html, bolnoy_html=bolnoy_html, old_html=old_html,
                           cnt_list_html=cnt_list_html, cnt_baran=cnt_baran, cnt_ovca=cnt_ovca,
                           cnt_little=cnt_little, cnt_bolnoy=cnt_bolnoy, cnt_old=cnt_old, evening_html_check=evening_html_check, cnt_list_html_e=cnt_list_html_e, stat_str_e=stat_str_e, baran_html_e=baran_html_e,
                           ovca_html_e=ovca_html_e, little_html_e=little_html_e, bolnoy_html_e=bolnoy_html_e, old_html_e=old_html_e, cnt_baran_e=cnt_baran_e, cnt_ovca_e=cnt_ovca_e,
                           cnt_little_e=cnt_little_e, cnt_bolnoy_e=cnt_bolnoy_e, cnt_old_e=cnt_old_e, data_html=data_html, stat_str_html_e=stat_str_html_e, stat_int=stat_int, stat_int_e=stat_int_e)


@application.route('/import_table', methods=['POST', 'GET'])
@login_required
def import_xls():
    global limit, defolt_limit, limit1, limit2, limit3, limit4
    limit = defolt_limit
    limit1 = defolt_limit
    limit2 = defolt_limit
    limit3 = defolt_limit
    limit4 = defolt_limit
    stat = db.execute("SELECT * from stat;")
    excel_type_check = 2
    delete_wrong_check = 0
    delete_wrong = None
    datestart = "2000-01-01"
    dateend = "2030-01-01"
    messages_file_not_found = [' ']  # ['File ".xlsx/.xls" did not found! Try again!']
    messages_success = [' ']
    messages_file_upload_error = [' ']
    messages_bd_error = [' ']
    messages_general = ['']
    messages_limit_value_error = ['']
    delete_copydate = 0
    if request.method == 'POST':
        limit = request.form.get('limitform')
        limit1 = request.form.get('limitform1')
        limit2 = request.form.get('limitform2')
        limit3 = request.form.get('limitform3')
        limit4 = request.form.get('limitform4')
        print(limit, limit1, limit2, limit3, limit4)

        try:
            limit = int(limit)
        except TypeError:
            limit = defolt_limit
        except ValueError:
            return render_template('import.html', messages_limit_value_error=messages_limit_value_error, stat=stat,
                                   defolt_limit=defolt_limit)
        try:
            limit1 = int(limit1)
        except TypeError:
            limit1 = defolt_limit
        except ValueError:
            return render_template('import.html', messages_limit_value_error=messages_limit_value_error, stat=stat,
                                   defolt_limit=defolt_limit)
        try:
            limit2 = int(limit2)
        except TypeError:
            limit2 = defolt_limit
        except ValueError:
            return render_template('import.html', messages_limit_value_error=messages_limit_value_error, stat=stat,
                                   defolt_limit=defolt_limit)
        try:
            limit3 = int(limit3)
        except TypeError:
            limit3 = defolt_limit
        except ValueError:
            return render_template('import.html', messages_limit_value_error=messages_limit_value_error, stat=stat,
                                   defolt_limit=defolt_limit)
        try:
            limit4 = int(limit4)
        except TypeError:
            limit4 = defolt_limit
        except ValueError:
            return render_template('import.html', messages_limit_value_error=messages_limit_value_error, stat=stat,
                                   defolt_limit=defolt_limit)

        print(limit, limit1, limit2, limit3, limit4)
        if 'file' not in request.files:
            return render_template('import.html', messages_file_upload_error=messages_file_upload_error, stat=stat)
        # if 'importxls' not in request.files:
        #   return render_template('import.html', messages_file_upload_error=messages_file_upload_error, stat=stat)
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            excel_name = filename
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        else:
            return render_template('import.html', messages_file_not_found=messages_file_not_found, stat=stat, defolt_limit=defolt_limit)
        failed1_print = 0
        try:
            con = psycopg2.connect(dbname='postgres', user='postgres',
                                 password='123456', host='localhost')
            # con = psycopg2.connect(dbname='new1', user='postgres',
            #                        password='Qwertyasdfsega161', host='localhost')
        except:
            return render_template('import.html', messages_bd_error=messages_bd_error, stat=stat)
            print('Не удалось подключиться к базе данных!')
        cur = con.cursor()

        excel_check = 0
        # while excel_check == 0:
        #   try:
        #      for file in os.listdir("./xls_upload"):
        #         if file.endswith(".xlsx"):
        #            excel_full_name = os.path.join("./xls_upload", file)
        #           excel_name = excel_full_name[13::]
        #      elif file.endswith(".xls"):
        #         excel_full_name = os.path.join("./xls_upload", file)
        #        excel_name = excel_full_name[13::]     #2
        # excel = open_workbook(excel_full_name)
        # sheet = excel.sheet_by_index(0)
        ###excel_type_check = 0
        # break
        # except:
        #   return render_template('import.html', messages_file_not_found=messages_file_not_found, stat=stat)
        # print('Файл ".xlsx/.xls" не найден! Попробуйте еще раз!')
        # break
        while excel_check == 0:
            try:
                excel_full_name = os.path.join("./xls_upload", filename)
                ##excel_full_name = os.path.join("./xls_upload", file)
                # for file in os.listdir("./xls_upload"):
                # if file.endswith(".xlsx"):
                # excel_full_name = os.path.join("./xls_upload", file)
                #   excel_name = excel_full_name[13::]
                # elif file.endswith(".xls"):
                # excel_full_name = os.path.join("./xls_upload", file)
                # excel_name = excel_full_name[13::]  # 2
                excel = open_workbook(excel_full_name)
                sheet = excel.sheet_by_index(0)
                excel_type_check = 0
                break
            except:
                return render_template('import.html', stat=stat)
                # print('Файл ".xlsx/.xls" не найден! Попробуйте еще раз!')
                break

        type1 = ''
        ccc = 0

        data_time = sheet.col_values(0)
        tagid = sheet.col_values(1)
        length = sheet.col_values(2)
        ant = sheet.col_values(3)
        cnt = sheet.col_values(4)
        rssi = sheet.col_values(5)
        try:
            tagid.remove('TagID')
            length.remove('Length')
            ant.remove('Ant')
            cnt.remove('Cnt')
            rssi.remove('RSSI')
            data_time.remove('Time')
            data_date = excel_name[8:12] + '-' + excel_name[12:14] + '-' + excel_name[14:16]
            print(data_date)
        except ValueError:
            messages_value_error = [' ']
            return render_template('import.html', messages_value_error=messages_value_error, stat=stat)

        type_check = 1
        time_of_day = ''

        now_time = datetime.datetime.now()
        for i in range(len(tagid)):
            if (tagid[i])[1] == '1':
                type1 = 'Баран'
                type_check = 0
                ccc = ccc + 1
            elif (tagid[i])[1] == '2':
                type_check = 0
                type1 = 'Овца'
                ccc = ccc + 1
            elif (tagid[i])[1] == '3':
                type_check = 0
                type1 = 'Ягненок'
                ccc = ccc + 1
            elif (tagid[i])[1] == '4':
                type_check = 0
                type1 = 'Больной'
                ccc = ccc + 1
            elif (tagid[i])[1] == '5':
                type_check = 0
                type1 = 'Старый'
                ccc = ccc + 1
            elif (tagid[i])[1] != '1' or (tagid[i])[1] != '2' or (tagid[i])[1] != '3' or (tagid[i])[1] != '4' or \
                    (tagid[i])[1] != '5':
                print('ошибка!!')
                type_check = 0
                type1 = 'Не определено'
            if data_time[i] < '13:00:00':
                time_of_day = 'morning'
            else:
                time_of_day = 'evening'

            # data_date_check = db.execute("SELECT data_date from test1")
            # time_of_day_check = db.execute("SELECT time_of_day from test1")
            #
            # for i in range(len(data_date_check)):
            #     if data_date_check[i] == data_date and time_of_day_check[i] == time_of_day:
            if delete_copydate == 0:
                try:
                    db.execute("DELETE from test1 WHERE data_date = %(data_date)s and time_of_day = %(time_of_day)s",
                               {'data_date': data_date, 'time_of_day': time_of_day})
                    delete_copydate = 1
                except:
                    pass

            try:
                cur.execute(
                    "INSERT INTO test1 (data_time, tag_id, lenght, ant, cnt, rssi, type, created_date, data_date, time_of_day) "
                    "VALUES (%(data_time)s, %(tag_id)s, %(lenght)s, %(ant)s, %(cnt)s, %(rssi)s, %(type)s, %(created_date)s, %(data_date)s, %(time_of_day)s)",
                    {'data_time': data_time[i], 'tag_id': tagid[i], 'lenght': length[i],
                     'ant': ant[i], 'cnt': cnt[i], 'rssi': rssi[i], 'type': type1, 'created_date': now_time,
                     'data_date': data_date, 'time_of_day': time_of_day})

            except psycopg2.errors.InvalidDatetimeFormat:
                messages_invalid_datetime_format = [' ']
                return render_template('import.html', messages_invalid_datetime_format=messages_invalid_datetime_format,
                                       stat=stat)
            except psycopg2.errors.DatetimeFieldOverflow:
                messages_invalid_datetime_format = [' ']
                return render_template('import.html', messages_invalid_datetime_format=messages_invalid_datetime_format,
                                       stat=stat)
        con.commit()
        db.execute("DELETE from test1 WHERE type = 'Не определено'")
        if type_check == 0:
            try:
                shutil.move(excel_full_name, './old_xls')
            except shutil.Error:
                for num in range(999):
                    try:
                        os.rename('./old_xls/' + excel_name, './old_xls/' + str(num) + excel_name)
                        shutil.move(excel_full_name, './old_xls')
                        break
                    except FileExistsError:
                        num += 1

            # result_set_import = (SELECT )
            # print('Добавление данных в таблицу БД выполнено успешно!')
            result_set = db.execute(
                "SELECT type, sum(count) as count FROM vw_stat where created_date > (now() - interval '5 second') group by type order by count desc;")
            result_set_cnt = db.execute(
                "SELECT sum(count) as count FROM vw_stat where created_date > (now() - interval '5 second') ;")
            # cnt_int = result = [int(item) for item in cnt]
            # cnt_sum = len(cnt_int)
            # print(cnt)
            # print(cnt_sum)
            db.execute("DELETE from stat; INSERT INTO stat (import_data, cnt) VALUES (%(import_data)s, %(cnt)s)",
                       {'import_data': now_time, 'cnt': ccc})
            stat = db.execute("SELECT * from stat;")
            result_set_check_01 = True
            return redirect(url_for('importdata', data_date=data_date))
            cur = con.cursor()
        else:
            messages_type_error = [' ']
            return render_template('import.html', messages_type_error=messages_type_error, stat=stat)
    return render_template('import.html', stat=stat, defolt_limit=defolt_limit)


@application.route('/importdata/<data_date>')
@login_required_user
def importdata(data_date):
    global limit, limit1, limit2, limit3, limit4
    stat = db.execute("SELECT * from stat;")
    messages_success = [' ']
    result_set_check_01 = True
    result_set_1 = db.execute(
        "SELECT type, sum(count) as count FROM vw_stat where created_date > (now() - interval '5 second') group by type order by count desc;")
    datereport = data_date
    dateformat = '%Y-%m-%d'
    month_html = None
    month_html_y = None

    # работа с датой "сегодня"
    today_html = dt.strptime(datereport, dateformat)

    day_t = today_html.day
    day_t = str(day_t)

    month_t = today_html.month
    month_t = str(month_t)

    if day_t == '1' or day_t == '2' or day_t == '3' or day_t == '4' or day_t == '5' or day_t == '6' or day_t == '7' or day_t == '8' or day_t == '9':
        day_t = '0' + day_t

    if month_t == '1' or month_t == '2' or month_t == '3' or month_t == '4' or month_t == '5' or month_t == '6' or month_t == '7' or month_t == '8' or month_t == '9':
        month_t = '0' + month_t

    # опредление месяца
    if month_t == '01':
        month_html = '.01'
    elif month_t == '02':
        month_html = '.02'
    elif month_t == '03':
        month_html = '.03'
    elif month_t == '04':
        month_html = '.04'
    elif month_t == '05':
        month_html = '.05'
    elif month_t == '06':
        month_html = '.06'
    elif month_t == '07':
        month_html = '.07'
    elif month_t == '08':
        month_html = '.08'
    elif month_t == '09':
        month_html = '.09'
    elif month_t == '10':
        month_html = '.10'
    elif month_t == '11':
        month_html = '.11'
    elif month_t == '12':
        month_html = '.12'

    # работа с датой "вчера"
    yesterday_html = dt.strptime(datereport, dateformat) - timedelta(days=1)

    day_y = yesterday_html.day
    day_y = str(day_y)

    month_y = yesterday_html.month
    month_y = str(month_y)

    if day_y == '1' or day_y == '2' or day_y == '3' or day_y == '4' or day_y == '5' or day_y == '6' or day_y == '7' or day_y == '8' or day_y == '9':
        day_y = '0' + day_y

    if month_y == '1' or month_y == '2' or month_y == '3' or month_y == '4' or month_y == '5' or month_y == '6' or month_y == '7' or month_y == '8' or month_y == '9':
        month_y = '0' + month_y

    # month = datereport[5:7]
    # day = datereport[8:10]
    # year = datereport[0:4]\
    # опредление месяца
    if month_y == '01':
        month_html_y = '.01'
    elif month_y == '02':
        month_html_y = '.02'
    elif month_y == '03':
        month_html_y = '.03'
    elif month_y == '04':
        month_html_y = '.04'
    elif month_y == '05':
        month_html_y = '.05'
    elif month_y == '06':
        month_html_y = '.06'
    elif month_y == '07':
        month_html_y = '.07'
    elif month_y == '08':
        month_html_y = '.08'
    elif month_y == '09':
        month_html_y = '.09'
    elif month_y == '10':
        month_html_y = '.10'
    elif month_y == '11':
        month_html_y = '.11'
    elif month_y == '12':
        month_html_y = '.12'

    # day_html = int(day)

    result_set = db.execute("select * from proc_one_day('" + datereport + "');")
    return render_template('import_data.html', result_set=result_set, result_set_1=result_set_1,
                           messages_success=messages_success, result_set_check_01=result_set_check_01, stat=stat,
                           month_html=month_html, month_html_y=month_html_y, day_t=day_t, day_y=day_y, limit=limit, limit1=limit1, limit2=limit2, limit3=limit3, limit4=limit4)


@application.route('/calendar', methods=['POST', 'GET'])
@login_required_user
def calendar():
    stat = db.execute("SELECT * from stat;")
    vecherom = [20, 170, 45]
    vecherom1 = 25
    vecherom2 = 40
    vecherom3 = 45
    check_graf = True
    vecheromnone = 85
    # utrom = [10, 170, 50]
    utrom1 = 25
    utrom2 = 35
    utrom3 = 55
    date_test = '2020-05-13'
    date_test1 = '2020-05-14'
    date_default = datetime.date.today()
    date_default_end = datetime.date.today()
    general_date = []
    utro_vars = []
    count_01 = []
    a = None
    if request.method == "POST":
        try:
            req = request.form
            datestart = request.form['dt_start']
            general_date.append(datestart)
            dateend = request.form['dt_end']
            general_date.append(dateend)

            result_set_date = db.execute(
                "SELECT type, sum(count) as count FROM vw_stat where date(date_req) between date('" + datestart + "') and date('" + dateend + "') group by type order by count desc;")
            if datestart > dateend:
                messages_wrong_date = [" "]  # ["The end date is earlier than the start date!"]
                return render_template('calendar.html', messages_wrong_date=messages_wrong_date,
                                       date_default=date_default, date_default_end=date_default_end, stat=stat)
            elif result_set_date.rowcount < 1:
                messages_empty_rows = [" "]  # ["There are no statistics for this time period!"]
                return render_template('calendar.html', messages_empty_rows=messages_empty_rows,
                                       date_default=date_default, date_default_end=date_default_end, stat=stat)
            # utrom = db.execute("SELECT date_req, utro_vecher, cnt FROM vw_stat_all where date(date_req) between date('" + datestart + "') and date('" + dateend + "') and utro_vecher = 'morning';")
            utrom = db.execute(
                "SELECT date_req, utro_vecher, cnt FROM proc_stat_all ('" + datestart + "','" + dateend + "') where utro_vecher = 'morning';")

            utromdb = db.execute(
                "SELECT date_req, utro_vecher, cnt FROM proc_stat_all ('" + datestart + "','" + dateend + "') where utro_vecher = 'morning';")

            utrom0 = []
            for i in utromdb:
                utrom0.append(i.cnt)

            # vecher = db.execute("SELECT date_req, utro_vecher, cnt FROM vw_stat_all where date(date_req) between date('" + datestart + "') and date('" + dateend + "') and utro_vecher = 'evening';")
            vecher = db.execute(
                "SELECT date_req, utro_vecher, cnt FROM proc_stat_all ('" + datestart + "','" + dateend + "') where utro_vecher = 'evening';")

            vecherdb = db.execute(
                "SELECT date_req, utro_vecher, cnt FROM proc_stat_all ('" + datestart + "','" + dateend + "') where utro_vecher = 'evening';")

            vecher1 = []
            for i in vecherdb:
                vecher1.append(i.cnt)

            date_list = db.execute(
                "SELECT distinct date_req FROM proc_stat_all('" + datestart + "','" + dateend + "') where date(date_req) between date('" + datestart + "') and date('" + dateend + "');")

            date_listdb = db.execute(
                "SELECT distinct date_req FROM proc_stat_all('" + datestart + "','" + dateend + "') where date(date_req) between date('" + datestart + "') and date('" + dateend + "');")

            date_list1 = []
            for i in date_listdb:
                date_list1.append(i.date_req)
            lenlist = len(date_list1)
            lenlist = int(lenlist)

            colordif = []
            for i in range(len(date_list1)):
                dif = int(utrom0[i]) - int(vecher1[i])
                if dif == 0:
                    colordif.append(0)
                elif dif > 0:
                    colordif.append(1)
                else:
                    colordif.append(2)

            date_default = datestart
            date_default_end = dateend
            return render_template('calendar.html', result_set_date=result_set_date, date_default=date_default,
                                   date_default_end=date_default_end, vecherom1=vecherom1,
                                   vecherom2=vecherom2, vecherom3=vecherom3, utrom1=utrom1, utrom2=utrom2,
                                   utrom3=utrom3, date_test=date_test, date_test1=date_test1,
                                   check_graf=check_graf, utrom=utrom, vecher=vecher, date_list=date_list, stat=stat, vecher1=vecher1, date_list1=date_list1, utrom0=utrom0, lenlist=lenlist, colordif=colordif)
        except:
            return render_template('calendar.html', date_default=date_default, date_default_end=date_default_end,
                                   stat=stat)
    else:
        return render_template('calendar.html', date_default=date_default, date_default_end=date_default_end, stat=stat)
    return render_template('calendar.html', date_default=date_default, date_default_end=date_default_end, stat=stat)


@application.route('/login', methods=['GET', 'POST'])
def login_page():
    if not session.get('logged_in') or not session.get('user'):
        stat = db.execute("SELECT * from stat;")
        success_messages = ['']
        warning_messages = ['']
        false_messages = ['']
        login_true = 'admin'
        password_true = 'admin'
        login_user = 'user'
        password_user = '123456'

        if request.method == "POST":
            login = request.form.get('InputLogin1')
            print(login)
            password = request.form.get('InputPassword1')
            print(password)
            remember_check = request.form.get('remember')

            if login_true == login and password_true == password:
                session['logged_in'] = True
                session['user'] = True
                if remember_check is None:
                    session.permanent = False
                else:
                    session.permanent = True
                return render_template('login.html', stat=stat, success_messages=success_messages)
            elif login_user == login and password_user == password:
                session['user'] = True
                if remember_check is None:
                    session.permanent = False
                else:
                    session.permanent = True
                return render_template('login.html', stat=stat, success_messages=success_messages)
            else:
                return render_template('login.html', stat=stat, false_messages=false_messages)


        else:
            return render_template('login.html', stat=stat)

        return render_template('login.html', stat=stat)
    else:
        return redirect(url_for('login_page'))


@application.route('/logout', methods=['GET', 'POST'])
def logout_page():
    success_logout_messages = ['']
    try:
        session.pop('user')
    except KeyError:
        return redirect(url_for('login_page'))
    try:
        session.pop('logged_in')
    except KeyError:
        return render_template('logout.html', success_logout_messages=success_logout_messages)

    return render_template('logout.html', success_logout_messages=success_logout_messages)


if __name__ == '__main__':
    ##application.run(debug=True)
    application.run(host='0.0.0.0', debug=True)
