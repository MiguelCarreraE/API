from flask import Flask, jsonify, request, abort
from datetime import datetime
app = Flask(__name__)

tasks = []
BASE_URL = '/api/v1/'


@app.route('/')
def home():
    return 'Welcome to my To-Do List'


@app.route(BASE_URL + 'tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(400,error='Missing body in requets')
    if 'name' in request.json:
        if 'category' in request.json:
            this_time=datetime.now()
            task={
                'id':len(tasks)+1,
                'name': request.json['name'],
                'category':request.json['category'],
                'status': False,
                'created': this_time,
                'updated':this_time,
            }
            tasks.append(task)
            return jsonify({'task':task}),201
        else:
            return jsonify({'404':'error'})
    else:
        return jsonify({'404':'error'})
    

@app.route(BASE_URL + 'tasks', methods=['GET'])
def get_tasks():
    return jsonify({'task':tasks})


@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_task(id):
    this_task=[task for task in tasks if task['id']==id]
    print("TASK")
    if len(this_task)==0:
        abort(404,error='ID not found')
    return jsonify({'task':this_task[0]})


@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def check_task(id):
    this_task=[task for task in tasks if task['id']==id]
    if len(this_task) == 0:
        abort(404, error="ID not found!")
    this_task[0]['status'] = not this_task[0]['status']
    return jsonify({'task': this_task[0]})

@app.route('/api/v1/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error="ID not found!")
    tasks.remove(this_task[0])
    return jsonify({'task': True})

if __name__ == "__main__":
    app.run(debug=True)