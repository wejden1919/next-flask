import json
from flask import Flask, jsonify, request
from db import execute_query
from user import user_is_valid

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    query = "SELECT * FROM users;"
    cursor, conn = execute_query(query)
    if cursor:
        rows = cursor.fetchall()
        columns=[desc[0] for desc in cursor.description]
        users = [{columns[0]: row[0], columns[1]: row[1], columns[2]: row[2],columns[3]:row[3]} for row in rows]
        
        print(columns)
        return jsonify(users)
    else:
        return jsonify({'error': 'Failed to retrieve users.'}), 500

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    query = "SELECT * FROM users WHERE id = %s;"
    cursor, conn = execute_query(query, (id,))
    if cursor:
        row = cursor.fetchone()
        if row:
            user = {'id': row[0], 'username': row[1], 'email': row[2],'password':row[3]}
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found.'}), 404
    else:
        return jsonify({'error': 'Failed to retrieve user.'}), 500

@app.route('/users', methods=['POST'])
def create_user():
    user_data = json.loads(request.data)
    if not user_is_valid(user_data):
        return jsonify({'error': 'Invalid user properties.'}), 400
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id;"
    values = (user_data['username'], user_data['email'], user_data['password'])
    cursor, conn = execute_query(query, values)
    if cursor:
        new_user_id = cursor.fetchone()[0]
        conn.commit()  
        return jsonify({'id': new_user_id}), 201
    else:
        return jsonify({'error': 'Failed to create user.'}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id: int):
    user_data = json.loads(request.data)
    if not user_is_valid(user_data):
        return jsonify({ 'error': 'Invalid user properties.' }), 400
    query = "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s;"
    values = (user_data['username'], user_data['email'], user_data['password'], id)
    cursor, conn = execute_query(query, values)
    if cursor:
        if cursor.rowcount > 0:
            conn.commit()  
            return jsonify({'message': 'User updated successfully.'}), 200
        else:
            return jsonify({'error': 'User not found or no changes were made.'}), 404
    else:
        return jsonify({'error': 'Failed to update user.'}), 500

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user_by_id(id:int):
    query = "DELETE FROM users WHERE id = %s;"
    cursor, conn = execute_query(query, (id,))
    if cursor:
        if cursor.rowcount > 0:
            conn.commit()  
            return jsonify({'message': 'User deleted successfully.'}), 200
        else:
            return jsonify({'error': 'User not found.'}), 404
    else:
        return jsonify({'error': 'Failed to delete user.'}), 500
    


if __name__ == '__main__':
    app.run(port=5000)