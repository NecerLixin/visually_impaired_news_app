from flask import Blueprint
from flask_socketio import emit,SocketIO,namespace
# from app import socketio

websocket_bp = Blueprint('audio', __name__)

socketio = SocketIO()

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