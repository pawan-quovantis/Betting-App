import json
import requests
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, request, redirect
from flask_login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUserMixin)
from models import *
from server import app, db
from flask import jsonify
import hashlib

parser = reqparse.RequestParser()
parser.add_argument('task')


class User(UserMixin):
    """User Session management Class
    """
    def __init__(self, email, id, fname="", lname="", accesstoken="", active=True):
        self.email = email
        self.id = id
        self.active = active
        self.fname = fname
        self.lname = lname
        self.accesstoken = accesstoken


USERS = {1: User("anurag@grexit.com", 1, "Anurag", "Maher", "", True)}

USER_NAMES = dict((u.email, u) for u in USERS.itervalues())


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"


@app.route("/")
def hello():
    if current_user.is_authenticated:
        return " User " + str(current_user.myemail()) + " is logged in "

    return "Hello World!"


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")


# @app.route("/login", methods=["GET", "POST"])

class Login(Resource):

    def get(self):
        from modules.oauth2 import GeneratePermissionUrl
        # if current_user.is_authenticated:
        #     return current_user.get_id()
        #
        # if request.method == "GET":
        #     useremail = request.args.get('email', '')
        #     if useremail:
        #         if useremail in USER_NAMES:
        #             loginit = login_user(USER_NAMES[useremail], remember="yes")
        #             return "user already exists and logged in"

        url = GeneratePermissionUrl(app.config['GOOGLE_CLIENT_ID'], request.args.get('email', ''),
                                    redirect_uri=app.config['REDIRECT_URI'],
                                    google_account_base_url=app.config['GOOGLE_ACCOUNTS_BASE_URL'])
        return url


@app.route("/oauth2callback", methods=["GET", "POST"])
def oauth2callback():
    from modules.oauth2 import AuthorizeTokens
    if request.method == "GET":
        authorization_code = request.args.get('code', '')
        response = AuthorizeTokens(app.config['GOOGLE_CLIENT_ID'],
                                   app.config['GOOGLE_CLIENT_SECRET'],
                                   authorization_code,
                                   redirect_uri=app.config['REDIRECT_URI'],
                                   google_account_base_url=app.config['GOOGLE_ACCOUNTS_BASE_URL'])
        access_token = response["access_token"]
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + access_token)
        j = json.loads(r.text)
        email = j.get("email")
        first_name = j.get("given_name")
        last_name = j.get("family_name")
        user_id = j.get("id")
        password = (hashlib.md5(str(user_id).encode('utf-8')).hexdigest())
        try:
            user = db.session.query(Users).filter(Users.password == password).first()
            if user is None:
                user = Users(first_name=first_name, last_name=last_name, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                return jsonify({"verification_id": password, "email": email, "first_name": first_name,
                                "last_name": last_name})
            else:
                return jsonify({"verification_id": user.password, "email": user.email, "first_name": user.first_name,
                                "last_name": user.last_name})

        except Exception as ex:
            return ex.message, 500

    else:
        return "Ony GET requests are allowed"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


if __name__ == "__main__":
    app.run(debug=True)
