curl -i -X POST -H 'Content-Type: application/json' -d '{"user": "testuser"}' 'http://127.0.0.1:5000/user'
# -> user as json
curl -i -X POST 'http://127.0.0.1:5000/list-add/testuser'
# -> list_id
curl -i -X POST -H 'Content-Type: application/json' -d '{"name": "test1", "description": "test2"}' 'http://127.0.0.1:5000/list/<list_id>'
# -> entry as json
curl -i -X GET 'http://127.0.0.1:5000/list/<list_id>'
# -> list as json
curl -i -X DELETE 'http://127.0.0.1:5000/list/<list_id>'
# -> statuscode
curl -i -X PUT -H 'Content-Type: application/json' -d '{"name": "test3", "description": "test4"}' 'http://127.0.0.1:5000/list/<list_id>/entry/<id>'
# -> entry as json
curl -i -X DELETE 'http://127.0.0.1:5000/list/<list_id>/entry/<id>'
# -> statuscode
curl -i -X GET 'http://127.0.0.1:5000/user'
# -> users as json
curl -i -X DELETE 'http://127.0.0.1:5000/user/<user>'
# -> statuscode