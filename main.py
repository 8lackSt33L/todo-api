"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]

todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list_id': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list_id': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list_id': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list_id': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE' ,'POST'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break

    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)

    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list_id'] == list_id])

    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 204

    elif request.method == 'POST':
        # add a new entry to the todo list with given id
        new_entry = request.get_json(force=True)

        # validate input
        if not new_entry or 'name' not in new_entry:
            abort(406)

        # create new todo entry
        entry = {
            'id': str(uuid.uuid4()),
            'name': new_entry['name'],
            'description': new_entry.get('description', ''),
            'list_id': list_id
        }

        # add to todos list
        todos.append(entry)

        print('Added new entry:', entry)

        return jsonify(entry), 201


# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    new_list = request.get_json(force=True)
    if not new_list or 'name' not in new_list:
        abort(406)

    print('Got new list to be added: {}'.format(new_list))

    # create id for new list
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)

    return jsonify(new_list), 201


# define endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)


# define endpoint for editing entries
@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_entry(entry_id):

    entry = None
    for i in todos:
        if i['id'] == entry_id:
            entry = i
            break

    if not entry:
        abort(404)

    if request.method == 'PATCH':
        new_entry = request.get_json(force=True)

        if not new_entry:
            abort(406)

        if 'name' in new_entry:
            entry['name'] = new_entry['name']

        if 'description' in new_entry:
            entry['description'] = new_entry['description']

        if 'list_id' in new_entry:
            entry['list_id'] = new_entry['list_id']
        
        return jsonify(entry), 200

    elif request.method == 'DELETE':
        todos.remove(entry)
        return '', 204
    



if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)