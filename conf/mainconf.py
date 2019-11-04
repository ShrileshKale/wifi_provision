from flask import Config
import os

class DevelopmentConfig(Config):
	MONGODB_DATABASE = 'wifi_db'
	MONGODB_HOST= '127.0.0.1'
	MONGODB_PORT = 27017
	MONGODB_USERNAME = 'wifi_user'
	MONGODB_PASSWORD = 'wifi_password_123'

	SECRET_KEY = "wifi_2O19quTDhgP"

	