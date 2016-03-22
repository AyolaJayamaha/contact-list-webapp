import os
import sqlite3
from hashlib import md5
from time import time
import simplejson as json
from flask import Flask, make_response, jsonify
from flask.ext import restful
from flask import g
from flask import request

app = Flask(__name__)
api = restful.Api(app)

PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(PATH, 'phone.db')

CREATE_INDEX_LIST = """
                    CREATE TABLE IF NOT EXISTS contacts(name TEXT PRIMARY KEY, phoneNo TEXT)
                    """

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    return db

def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    query_type = query.lower().strip().split()[0]
    r = None
    if query_type == "select":
        r = cursor.fetchall()
    elif query_type in [ "update", "insert", "replace" ]:
        r = cursor.rowcount    
    get_db().commit()
    cursor.close()
    if query_type == "select" and r and one:
        return r[0]
    return r


def create_contact(name,phone):
    SQL = "INSERT INTO contacts VALUES(?, ?)"
    query_db(SQL, (name, phone,))


@app.before_first_request
def create_index_list():
    query_db(CREATE_INDEX_LIST)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def modeling(dataAll):
    all = [];
    if list == type(dataAll):
       for row in dataAll:
           all.append(row_modeling(row))
    return {'contacts' : all};

def row_modeling(row):
    return {"name": row[0], "phoneNo": row[1]}

def check_contact(name):
    SQL1 = 'SELECT * FROM contacts WHERE name = \''+name+'\'';
    rx = query_db(SQL1)
    if len(rx)>0:
        return True
    return False

#Access-Control-Allow-Origin only for to get as it is using in web app
class Home(restful.Resource):

    def get(self):
        SQL = 'SELECT * FROM contacts'
        r = query_db(SQL)
        contacts = modeling(r);
        resp = make_response(jsonify(contacts),200)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp;

class Admin(restful.Resource):

    def get(self, name):
        #checking contact is existing
        if check_contact(name):
            SQL = 'SELECT * FROM contacts WHERE name = \''+name+'\' LIMIT 1';
            r = query_db(SQL)
            contacts = modeling(r);
            return (jsonify(contacts));
        else:
            msg = name+' does not exist in contacts'
            return {'status': msg}

    def delete(self, name):
        #checking contact is existing before deleting
        if check_contact(name):
            SQL = 'DELETE FROM contacts WHERE name = \''+name+'\'';
            query_db(SQL)
            msg = name+' contact is deleted'
        else:
            msg = name+' does not exist in contacts'
        return {'status': msg}

class Update_Admin(restful.Resource):


    def post(self, name, phoneNo):
        create_contact(name,phoneNo)
        return {'status': name+' added to the contacts'}

    def put(self, name, phoneNo):
        #checking contact is existing before updating
        if check_contact(name):
            SQL = 'UPDATE contacts SET phoneNo = \''+phoneNo+'\' WHERE name = \''+name+'\'';
            r = query_db(SQL)
            msg = name+' contact is updated'
        else:
            msg = name+' does not exist in contacts'
        return {'status': msg}



api.add_resource(Home, '/')
api.add_resource(Update_Admin, '/<string:name>/<string:phoneNo>')
api.add_resource(Admin, '/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
