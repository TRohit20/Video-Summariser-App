from flask import Flask
from routes.transcribe import transcribe_route
from routes.test import test_route

app = Flask(__name__)

app.register_blueprint(transcribe_route)
app.register_blueprint(test_route)

if __name__ == '__main__':
    app.run()