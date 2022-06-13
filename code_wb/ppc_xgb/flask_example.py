from flask import Flask

app = Flask(__name__)

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

app.run(port=5001)
