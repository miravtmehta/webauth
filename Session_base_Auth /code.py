from flask import Flask, request
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.update(
    SECRET_KEY={'Nkey': 'Nvalue'},
)

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    "username": generate_password_hash("password"),
}


class User(UserMixin):

    @login_manager.user_loader
    def user_loader(self, username):
        if username in users:
            user_model = User()
            user_model.id = username
            return user_model
        return None

    @app.route("/page", methods=["POST"])
    def login_page(self):
        data = request.get_json()
        print(data)
        username = data.get("username")
        password = data.get("password")

        if username in users:
            if check_password_hash(users.get(username), password):
                user_model = User()
                user_model.id = username
                login_user(user_model)
            else:
                return "Wrong credentials"
        return "logged in"

    @app.route("/")
    @login_required
    def protected(self):
        return f"Current user: {current_user.id}"


if __name__ == "__main__":
    app.run()
