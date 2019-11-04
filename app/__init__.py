from flask import Flask, render_template
from flask_mongokit import MongoKit
from flask_socketio import SocketIO, emit, send, join_room
import json
from bson import json_util
from flask_cors import CORS

app = Flask(__name__)

socketio = SocketIO(app)

@socketio.on('connect', namespace="/spirograph")
def handle_connect():
	join_room('spirograph_room')
	send(json.dumps({
		"message": "Spirograph connected successfully",
		"status": True
		}, default=json_util.default))

CORS(app)

app.config.from_object('conf.mainconf.DevelopmentConfig')

db = MongoKit(app)

import api