import os.path
import sqlite3
import json
from flask import Flask, g, render_template, request, url_for, redirect
import run

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bluetooth.sqlite3")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        cur = get_db().cursor()
        count = cur.execute("select * from sqlite_master where type='table'")
        table_list = [row[1][10:] for row in count]
        return render_template('index.html', list=table_list)
    else:
        return redirect(url_for("/asdas"))


@app.route('/characteristics', methods=['GET'])
def characteristics():
    if request.method == 'GET':
        return render_template('characteristics.html', url="Bluetooth_characteristics")


@app.route('/services')
def services():
    return render_template('services.html', url="Bluetooth_services")


@app.route('/generic_access_profile')
def generic_access_profile():
    return render_template('generic_access_profile.html')


@app.route('/update')
def update():
    return run


@app.route('/api/<table>', methods=['POST', 'GET'])
def api(table):
    if request.method == 'GET':
        page = int(request.args.get("page"))
        limit = int(request.args.get("limit"))
        start = limit * (page - 1)
        cur = get_db().cursor()
        count = cur.execute("select count(*) from %s" % table).fetchone()
        res = cur.execute("select * from %s limit %s offset %s" % (table, limit, start))
        data = [dict(Name=row[0], Uniform_Type_Identifier=row[1], Assigned_Number=row[2], Specification=row[3])
                for row in res.fetchall()]
        rs = {'code': 0, 'count': count, 'data': data}
        return json.dumps(rs, ensure_ascii=False)
    else:
        code = request.form.get("Assigned_Number")
        cur = get_db().cursor()
        res = cur.execute('select * from %s where "Assigned Number"="%s"' % (table, code))
        data = [dict(Name=row[0], Uniform_Type_Identifier=row[1], Assigned_Number=row[2], Specification=row[3])
                for row in res.fetchall()]
        rs = {'code': 0, 'data': data}
        return json.dumps(rs, ensure_ascii=False)


@app.route('/api/generic_access_profile', methods=['POST', 'GET'])
def api_1():
    if request.method == 'GET':
        page = int(request.args.get("page"))
        limit = int(request.args.get("limit"))
        start = limit * (page - 1)
        cur = get_db().cursor()
        count = cur.execute("select count(*) from Bluetooth_generic_access_profile").fetchone()
        res = cur.execute("select * from Bluetooth_generic_access_profile limit %s offset %s" % (limit, start))
        data = [dict(Data_Type_Value=row[0], Data_Type_Name=row[1], Reference_for_Definition=row[2])
                for row in res.fetchall()]
        rs = {'code': 0, 'count': count, 'data': data}
        return json.dumps(rs, ensure_ascii=False)
    else:
        code = request.form.get("Data_Type_Value")
        cur = get_db().cursor()
        res = cur.execute('select * from Bluetooth_generic_access_profile where "Data Type Value"="%s"' % code)
        data = [dict(Data_Type_Value=row[0], Data_Type_Name=row[1], Reference_for_Definition=row[2])
                for row in res.fetchall()]
        rs = {'code': 0, 'data': data}
        return json.dumps(rs, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
