from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': '34.58.81.11',
    'user': 'ragul',
    'password': '12345',
    'database': 'taskdb'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    description = data.get('description')
    status = data.get('status', 'pending')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (description, status) VALUES (%s, %s)', (description, status))
    conn.commit()
    cursor.close()
    conn.close()
    return 'Task created', 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    status = data.get('status')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = %s WHERE id = %s', (status, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return 'Task updated'

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return 'Task deleted'

if __name__ == '__main__':
    try:
        conn = get_db_connection()
        conn.ping(reconnect=True, attempts=1, delay=0)
        print('✅ Successfully connected to the database.')
        conn.close()
        app.run(debug=True, host='0.0.0.0', port=3000)
    except mysql.connector.Error as err:
        print('❌ Failed to connect to the database:', err)
