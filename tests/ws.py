from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return "WebSocket Server is running. Connect to it using a WebSocket client."

# @socketio.on('connect', namespace='/audio')
# def handle_connect():
#     print('Client connected')
#     return '1'

@socketio.on('disconnect', namespace='/audio')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('open', namespace='/audio')
def handle_open():
    print('Client open')
    
@socketio.on('message', namespace='/audio')
def handle_message(msg):
    print(msg)

@socketio.on('audio_data', namespace='/audio')
def handle_audio_data(data):
    # Process and forward audio data
    emit('audio_response', data, broadcast=True)
    
if __name__ == "__main__":
    print(1111)
    socketio.run(app, host='127.0.0.1', port=5001,debug=True)
    print(1111)
