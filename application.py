# -*- coding: UTF-8 -*-
from flask import Flask, render_template, url_for, app, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import datetime, xlrd, os, shutil
from xlrd import open_workbook
from shutil import move
import psycopg2


db = create_engine('postgresql://postgres:123456@localhost:5432/postgres')



application = Flask(__name__)
application.config['SQLALCHEMY_DTABASE_URI'] = "posgresql://postgres:123456@localhost:5432/postgres"
#db = SQLAlchemy(app)


@application.route('/')
@application.route('/main')
def index():
    datestart = "2000-01-01"
    dateend = "2030-01-01"
    result_set = db.execute("SELECT type, sum(count) as count FROM vw_stat where date(date_req) between date('" + datestart + "') and date('" + dateend + "') group by type order by count desc;")
    return render_template('about.html', result_set=result_set)


@application.route('/import_table', methods=['POST', 'GET'])
def import_xls():
    excel_type_check = 2
    datestart = "2000-01-01"
    dateend = "2030-01-01"
    messages_file_not_found = ['Файл ".xlsx/.xls" не найден! Попробуйте еще раз!']
    messages_success = ['Добавление данных в таблицу БД выполнено успешно!']
    messages_bd_error = ['Не удалось подключиться к БД!']
    messages_general = ['Загружено:']
    if request.method == 'POST':
        failed1_print = 0
        try:
            con = psycopg2.connect(dbname='new1', user='postgres',
                                   password='Qwertyasdfsega161', host='localhost')
        except:
            return render_template('import.html', messages_bd_error=messages_bd_error)
            print('Не удалось подключиться к базе данных!')
        cur = con.cursor()
        excel_check = 0
        while excel_check == 0:
            try:
                for file in os.listdir("./"):
                    if file.endswith(".xlsx"):
                        excel_full_name = os.path.join("./", file)
                        excel_name = excel_full_name[2::]
                    elif file.endswith(".xls"):
                        excel_full_name = os.path.join("./", file)
                        excel_name = excel_full_name[2::]
                excel = open_workbook(excel_full_name)
                sheet = excel.sheet_by_index(0)
                #excel_type_check = 0
                break
            except:
                return render_template('import.html', messages_file_not_found=messages_file_not_found)
                #print('Файл ".xlsx/.xls" не найден! Попробуйте еще раз!')
                break


        now_time = datetime.datetime.now()

        type1 = ''

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
        except ValueError:
            messages_value_error = [' В данном .xls/.xlsx файле, отсутствуют имена всех или одних из данных колонок: (Time/TagID/Length/Ant/Cnt/RSSI). Либо же, они были введены неправильно!']
            return render_template('import.html', messages_value_error=messages_value_error)

        type_check = 1

        for i in range(len(tagid)):
            if (tagid[i])[1] == '1':
                type1 = 'Мужчина'
                type_check = 0
            elif (tagid[i])[1] == '2':
                type_check = 0
                type1 = 'Женщина'
            elif (tagid[i])[1] == '3':
                type_check = 0
                type1 = 'Ребенок'
            elif (tagid[i])[1] == '4':
                type_check = 0
                type1 = 'Инвалид'
            elif (tagid[i])[1] == '5':
                type_check = 0
                type1 = 'Пенсионер'
            elif (tagid[i])[1] == '1' or (tagid[i])[1] == '2' or (tagid[i])[1] == '3' or (tagid[i])[1] == '4' or (tagid[i])[1] == '5':
                messages_type_error = [' Не удалось определить "type" по значениям в колонке "TagID"!']
                return render_template('import.html', messages_type_error=messages_type_error)
                type_check = 1
                break

            try:
                cur.execute("INSERT INTO test1 (data_time, tag_id, lenght, ant, cnt, rssi, type, created_date, data_date) VALUES (%(data_time)s, %(tag_id)s, %(lenght)s, %(ant)s, %(cnt)s, %(rssi)s, %(type)s, %(created_date)s, %(data_date)s)",
                    {'data_time': data_time[i], 'tag_id': tagid[i], 'lenght': length[i],
                        'ant': ant[i], 'cnt': cnt[i], 'rssi': rssi[i], 'type': type1, 'created_date': now_time,
                        'data_date': data_date})
            except psycopg2.errors.InvalidDatetimeFormat:
                messages_invalid_datetime_format = [' Не удалось верно определить дату по названию файла!']
                return render_template('import.html', messages_invalid_datetime_format=messages_invalid_datetime_format)
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

            #result_set_import = (SELECT )
            con.commit()
            #print('Добавление данных в таблицу БД выполнено успешно!')
            result_set = db.execute("SELECT type, sum(count) as count FROM vw_stat where created_date > (now() - interval '10 second') group by type order by count desc;")
            #result_set = db.execute("SELECT 'hello kitty' as type, '10' as count;")
            return render_template('import.html', messages_success=messages_success, messages_general=messages_general, result_set=result_set)
            cur = con.cursor()
        else:
            messages_type_error = [' Не удалось определить "type" по значениям в колонке "TagID"!']
            return render_template('import.html', messages_type_error=messages_type_error)
    return render_template('import.html')


@application.route('/calendar', methods=['POST', 'GET'])
def calendar():
    date_default = datetime.date.today()
    date_default_end = datetime.date.today()
    a = None
    if request.method == "POST":
        try:
            req = request.form
            datestart = request.form['dt_start']
            dateend = request.form['dt_end']
            result_set_date = db.execute("SELECT type, sum(count) as count FROM vw_stat where date(date_req) between date('" + datestart + "') and date('" + dateend + "') group by type order by count desc;")
            #print(result_set_date)
            #for i in result_set_date:
            #    count_check = i.count
            #    print(count_check)
            #    type_check = i.type
            #    print(type_check)
            if datestart > dateend:
                messages_wrong_date = ["Дата конца раньше, чем дата начала!"]
                return render_template('calendar.html', messages_wrong_date=messages_wrong_date, date_default=date_default, date_default_end=date_default_end)
            elif result_set_date.rowcount < 1:
                messages_empty_rows = ["Статистика за этот период времени отсутсвует!"]
                return render_template('calendar.html', messages_empty_rows=messages_empty_rows, date_default=date_default, date_default_end=date_default_end)

            date_default = datestart
            date_default_end = dateend
            return render_template('calendar.html', result_set_date=result_set_date, date_default=date_default, date_default_end=date_default_end)
        except:
            return render_template('calendar.html', date_default=date_default, date_default_end=date_default_end)
    else:
        return render_template('calendar.html', date_default=date_default, date_default_end=date_default_end)
    return render_template('calendar.html', date_default=date_default, date_default_end=date_default_end)



@application.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'user: ' + name + '-' + str(id)


if __name__ == '__main__':
    application.run(debug=False)
