import json
from urllib import response
import uuid
import pprint
from flask import Flask, request, Response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
users = {}
lists = []

@app.route('/list/<list_id>',methods = ['GET'])
def list(list_id):
    for v in lists:
        if v[0]['list_id'] == list_id:
            j = json.dumps(v)
            return j

    return 'Statuscode: 404'

@app.route('/list-add/<user>',methods = ['GET'])
def list_add(user):
    d = {}
    d['user_id'] = users[user]
    d['list_id'] = str(uuid.uuid4())
    l = []
    l.append(d)
    lists.append(l)
    d2 = d
    d2['Statuscode'] = 200

    return str(d2)

@app.route('/list-delete/<list_id>',methods = ['GET'])
def list_delete(list_id):
    f = 404
    for v in lists:
        if v[0]['list_id'] == list_id:
            f = 200
            lists.remove(v)
    
    return str(f)

@app.route('/list-add-entry/<list_id>',methods = ['GET'])
def list_add_entry(list_id):
    for v in lists:
        if v[0]['list_id'] == list_id:
            d = {}
            d['id'] = str(uuid.uuid4())
            d['name'] = request.args.get('name')
            d['description'] = request.args.get('description')
            d['user_id'] = v[0]['user_id']
            d['list_id'] = list_id
            if "id" not in v[0]:
                v.remove(v[0])
            v.append(d)
            d2 = d
            d2['Statuscode'] = 200
            return str(d2)
    return 'Statuscode: 404' 

@app.route('/list-delete-entry/<id>',methods = ['GET'])
def list_delete_entry(id):
    f = 404
    for v in lists:
        for v2 in v:
            if v2['id'] == id:
                f = 200
                lists.remove(v2)
    
    return str(f)

@app.route('/list-change-entry/<list_id>/entry/<id>',methods = ['GET'])
def list_change_entry(list_id, id):
    for v in lists:
        if v[0]['list_id'] == list_id:
            for v2 in v:
                if v2['id'] == id:
                    v2['name'] = request.args.get('name')
                    v2['description'] = request.args.get('description')
                    d = v2
                    d['Statuscode'] = 200
                    return str(d)
                    
    return 'Statuscode: 404'    

@app.route('/user-add/<user>',methods = ['GET'])
def user_add(user):
    users[user] = str(uuid.uuid4())
    
    return str(users[user]) + ' Statuscode: 200'

@app.route('/user-delete/<user>',methods = ['GET'])
def user_delete(user):
    f = 0
    f = users.pop(user, f)
    if f == 0: f = 404
    elif f != 0: f = 200
    
    return str(f)

@app.route('/user-list',methods = ['GET'])
def user_list():
    return users

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
