import os
from flask import Flask
from routes import my_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

app.register_blueprint(my_routes)

if __name__ == '__main__':
    app.run()
