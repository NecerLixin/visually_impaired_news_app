from flask import Blueprint
from flask_socketio import emit
from .. import socketio

websocket_bp = Blueprint('websocket_bp', __name__)

@socketio.on('connect', namespace='/audio/a')
def handle_connect():
    print('Client connected')

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
