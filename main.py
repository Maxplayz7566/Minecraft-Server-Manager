import os
import sqlite3

import requests
import webview
from flask import Flask, send_from_directory, abort, request, jsonify
from flask_socketio import SocketIO
import kthread
import psutil

import serverjars

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_dir_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                file_size = os.path.getsize(fp)
                total_size += file_size

    total_size_mb = total_size / (1024 ** 2)
    total_size_gb = total_size / (1024 ** 3)

    if total_size_gb >= 1:
        return str(round(total_size_gb)) + ' GB'
    else:
        return str(round(total_size_mb)) + ' MB'

@socketio.on('connect')
def handleConnect():
    data = {
        'session': request.sid,
        'baseurl': request.base_url,
        'authorization': request.authorization
    }

    print(f'Client connected {data}')
    socketio.emit('connect', to=request.sid)

@socketio.on('requestmem')
def request_memory(data=None):
    process = psutil.Process()
    memory_info = process.memory_info().rss
    memory_in_mib = memory_info / 1.048576e+6
    socketio.emit('memory', round(memory_in_mib, 2), to=request.sid)

@socketio.on('requestdisk')
def request_disk(data=None):
    socketio.emit('diskusage', get_dir_size('servers'), to=request.sid)

@app.route('/api/getservers')
def getservers_api():
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM Servers'
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows

@app.route('/api/renameserver', methods=['PUT'])
def renameserver_api():
    server_id = request.args.get('id')
    new_name = request.args.get('name')

    if not server_id or not new_name:
        return 'Missing server ID or new name', 400

    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()

    # Check if the server exists
    cursor.execute('SELECT name FROM Servers WHERE id = ?', (server_id,))
    server = cursor.fetchone()
    if server is None:
        conn.close()
        return 'Server not found', 404

    # Update the server's name
    update_sql = '''
    UPDATE Servers
    SET name = ?
    WHERE id = ?
    '''
    cursor.execute(update_sql, (new_name, server_id))
    conn.commit()

    conn.close()

    return '', 204

@app.route('/api/addserver', methods=['POST'])
def addserver_api():
    name = request.args.get('name')
    port = request.args.get('port')

    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()

    insert_sql = '''
    INSERT INTO Servers (name, port)
    VALUES (?, ?)
    '''

    cursor.execute(insert_sql, (name, port))
    conn.commit()

    # Fetch the ID of the newly inserted server
    cursor.execute('SELECT id FROM Servers WHERE name = ? ORDER BY id DESC LIMIT 1', (name,))
    server_id = cursor.fetchone()[0]

    # Create the directory for the server
    os.makedirs(f'servers/{server_id}', exist_ok=True)

    conn.close()

    return '', 201

@app.route('/api/deleteserver', methods=['DELETE'])
def deleteserver_api():
    server_id = request.args.get('id')

    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()

    # Fetch the server's name to use for directory removal
    cursor.execute('SELECT name FROM Servers WHERE id = ?', (server_id,))
    server = cursor.fetchone()
    if server is None:
        conn.close()
        return 'Server not found', 404

    server_name = server[0]

    # Delete the server entry from the database
    cursor.execute('DELETE FROM Servers WHERE id = ?', (server_id,))
    conn.commit()

    # Remove the directory for the server
    server_dir = f'servers/{server_id}'
    if os.path.exists(server_dir):
        os.rmdir(server_dir)

    conn.close()

    return '', 204

@app.route('/')
def root():
    return send_from_directory('web', 'index.html')

@app.route('/<path:filepath>')
def serve_file(filepath):
    base_directory = 'web'
    full_path = os.path.join(base_directory, filepath)

    if filepath.endswith('/'):
        index_path = os.path.join(full_path, 'index.html')
        print(f"Index path: {index_path}")
        if os.path.isfile(index_path):
            return send_from_directory(full_path, 'index.html')
        else:
            abort(404)

    if os.path.isfile(full_path):
        return send_from_directory(base_directory, filepath)
    else:
        abort(404)

def main():
    flaskThread.start()

if __name__ == "__main__":
    flaskThread = kthread.KThread(target=lambda: (
        app.run(host="0.0.0.0", port=80)
    ), daemon=True)
    window = webview.create_window('Minecraft Server Manager',
                                   server=None,
                                   url='http://localhost:80/index.html',
                                   frameless=True,
                                   easy_drag=True,
                                   resizable=False,
                                   width=900,
                                   height=600,
                                   shadow=True,
                                   vibrancy=True
                                   )

    webview.start(main, http_server=False, private_mode=True)
