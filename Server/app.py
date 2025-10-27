import json
import os
from functools import wraps
from flask import Flask, request, make_response, jsonify
from pymongo import MongoClient
import jwt
import random

app = Flask(__name__)

#generating secret key
key = str(random.SystemRandom().getrandbits(128))
app.config['SECRET_KEY'] = key
print(key)
key = 'used'
password = os.getenv('PASSWORD')
#creating database
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://statserv-mongo:27017/'))
statdb = client['statdb']
stat_collection = statdb['stats']
prog_collection = statdb['progress']
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
def token_check(f):
    @wraps(f)
    def guard(*args, **kwargs):
        token = request.args.get('token')
        role = request.args.get('role')
        if token is None:
            return make_response('Token is missing', 401)
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return f(*args, **kwargs)
    return guard
@app.route('/auth', methods=['POST'])
def auth():
    host = request.args.get('host')
    role = request.args.get('role')
    if role == 'script':
        token = jwt.encode({'user' : host, 'role' : 'script'}, app.config['SECRET_KEY'])
        return make_response(token)
    elif role == 'admin':
        auth = request.args.get('password')
        if auth == password:
            token = jwt.encode({'user' : host, 'role' : 'admin'}, app.config['SECRET_KEY'])
            return make_response(token)
        return make_response('Authentication denied', 401)
    else:
        return make_response('Authentication denied', 401)
@app.route('/client', methods=['POST'])
@token_check
def client():
    data = request.get_json()
    host = data.get('host')
    type = request.args.get('data')
    print('Incoming data type:', request.args.get('data'))
    if type == 'stats':
        if stat_collection.find_one({'host': host}) is None:
            stat_collection.insert_one(request.get_json())
        else:
            update_operation = {'$set': data}
            stat_collection.update_one({'host': host}, update_operation)
    elif type == 'prog':
        if prog_collection.find_one({'host': host}) is None:
            prog_collection.insert_one(request.get_json())
        else:
            update_operation = {'$set': data}
            prog_collection.update_one({'host': host}, update_operation)
    else:
        return make_response('Invalid request', 401)
    return {'message': 'Info received!'}

@app.route('/admin', methods=['GET'])
@token_check
def admin():
    func = request.args.get('action')
    match func:
        case 'view_all':
            stats = list(stat_collection.find())
            prog = list(prog_collection.find())
            combined = {
                "stats": stats,
                "prog": prog
            }
            return json.dumps(combined, default=str)
        case 'view_user':
            try:
                print(request.args.get('user'))
                print(stat_collection.find_one({'host' : request.args.get('user')}))
                return json.dumps(stat_collection.find_one({'host' : request.args.get('user')}), default=str)
            except:
                return jsonify({'code': 404})
        case 'delete_user':
            try:
                prog_collection.delete_one({'host' : request.args.get('user')})
                stat_collection.delete_one({'host' : request.args.get('user')})
                return jsonify({'message': 'User deleted!'})
            except Exception:
                return jsonify({'message': 'User does not exist!'})
        case 'delete_metric':
            host = request.args.get('user')
            metric = request.args.get('metric')
            try:
                update_operation = {'$set': {metric : "N/A"}}
                stat_collection.update_one({'host': host}, update_operation)
                return jsonify({'code' : 200})
            except Exception:
                return jsonify({'code': 404})
        case _:
            return make_response('Invalid action', 401)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
