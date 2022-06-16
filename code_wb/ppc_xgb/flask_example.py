from flask import Flask, request
from flask_restx import Api, Resource


app = Flask(__name__)
api = Api(app)


# http://127.0.0.1:5001/
@app.route('/')
def index():
    return {
        "msg": "success",
        "data": "welcome to use flask."
    }

# http://127.0.0.1:5001/user/3
@app.route('/user/<u_id>')
def user_info(u_id):
    return {
        "msg": "success",
        "data": {
            "id": u_id,
            "username": 'yuz',
            "age": 18
        }
    }


# http://127.0.0.1:5001/hello
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {'1': 'abc', '2': '123'}
# todos = {}


# http://127.0.0.1:5001/1
@api.route('/<string:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


# http://127.0.0.1:5001/todo1
@api.route('/todo1')
class Todo1(Resource):
    def get(self):
        # Default to 200 OK
        return {'task': 'Hello world'}


# http://127.0.0.1:5001/todo2
@api.route('/todo2')
class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201


# http://127.0.0.1:5001/todo3
@api.route('/todo3')
class Todo3(Resource):
    def get(self):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}


if __name__=="__main__":
    app.run(port=5001)
