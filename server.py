from flask_app import app
from flask_app.controllers import users, characters

if __name__ == "__main__":
    app.run_server(host="18.188.64.225")