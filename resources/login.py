import json
import requests
from flask_restful import reqparse, Resource
from flask import request, jsonify, redirect, url_for
from models import *
from server import app, db
import hashlib
import datetime
import urllib

parser = reqparse.RequestParser()
parser.add_argument('task')


# test route
@app.route("/")
def hello():
    return "Hello World!"


class Login(Resource):

    def get(self):
        from modules.oauth2 import GeneratePermissionUrl
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

        if str(j.get("hd")) != 'quovantis.com':
            return "Emails registered only with Quovantis are allowed..."
        try:
            user = db.session.query(Users).filter(Users.password == password).first()
            print urllib.urlencode({"verification_id": user.password, "email": user.email, "first_name": user.first_name,
                              "last_name": user.last_name})
            if user is None:
                user = Users(first_name=first_name, last_name=last_name, email=email, password=password,
                             join_date=datetime.datetime.now())
                db.session.add(user)
                db.session.commit()

                # return redirect("/bets")
                # Not sure if this would work 
                return redirect("localhost:3000/dashboard")
                # , Response=jsonify({"verification_id": password, "email": email, "first_name": first_name,
                #                 "last_name": last_name}))
                # response = redirect('https://google.com')
                # response.headers = {'authorization': 'whatever'}
                # return response

            else:
                return redirect("localhost:3000/dashboard")
                # return redirect("/bets")
                # return redirect("/bets?"+str(urllib.urlencode({"verification_id": user.password, "email": user.email,
                # "first_name": user.first_name,
                #                 "last_name": user.last_name})))
                # return response

        except Exception as ex:
            return ex.message, 500

    else:
        return "Ony GET requests are allowed"

