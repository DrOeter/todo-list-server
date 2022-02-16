import json
from urllib import response
import uuid
import pprint
from flask import Flask, request, Response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
users = {}
lists = []

@app.route('/list-add/<user_id>',methods = ['POST'])
def list_add(user_id):
    #list-add
    for i, v in users.items():
        if v == user_id:
            d = {}
            d['user_id'] = user_id
            d['list_id'] = str(uuid.uuid4())
            l = []
            l.append(d)
            lists.append(l)

            return str(d) + ' Statuscode: 200'
    return 'Statuscode: 404'
    

@app.route('/list/<list_id>',methods = ['GET', 'POST', 'DELETE'])
def list(list_id):
    #list
    if request.method == 'GET':
        for v in lists:
            if v[0]['list_id'] == list_id:
                j = json.dumps(v)
                return j
    #list-delete
    if request.method == 'DELETE':
        f = 404
        for v in lists:
            if v[0]['list_id'] == list_id:
                f = 200
                lists.remove(v)
    
        return str(f)
    #list-add-entry
    if request.method == 'POST':
        data = json.loads( request.data )
        for v in lists:
            if v[0]['list_id'] == list_id:
                d = {}
                d['id'] = str(uuid.uuid4())
                d['name'] = data['name']
                d['description'] = data['description']
                d['user_id'] = v[0]['user_id']
                d['list_id'] = list_id
                if "id" not in v[0]:
                    v.remove(v[0])
                v.append(d)
                return str(d) + ' Statuscode: 200' 

    return 'Statuscode: 404'

@app.route('/list/<list_id>/entry/<id>',methods = ['PUT', 'DELETE'])
def list_entry(list_id, id):
    #entry-delete
    if request.method == 'DELETE':
        f = 404
        for v in lists:
            if v[0]['list_id'] == list_id:
                for v2 in v:
                    if v2['id'] == id:
                        f = 200
                        v.remove(v2)
        
        return str(f)
    #entry-change
    if request.method == 'PUT':
        data = json.loads( request.data )
        for v in lists:
            if v[0]['list_id'] == list_id:
                for v2 in v:
                    if v2['id'] == id:
                        v2['name'] = data['name']
                        v2['description'] = data['description']
                        return str(v2) + ' Statuscode: 200' 
                        
    return 'Statuscode: 404'    

@app.route('/user',methods = ['GET', 'POST'])
def user():
    #user-add
    if request.method == 'POST':
        user = json.loads( request.data )['user']
        if user not in users:
            users[user] = str(uuid.uuid4())
            return str(users[user]) 
    #user-list
    if request.method == 'GET':
        return users
            
    return 'Statuscode: 409'

@app.route('/user/<user_id>',methods = ['DELETE'])
def user_delete(user_id):
    #user-delete
    f = 404
    for key, value in users.items():
        if value == user_id:
            del users[key]
            f = 200
            break
    
    return str(f)

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
