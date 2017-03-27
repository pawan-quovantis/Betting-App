from flask_restful import Resource
from models import *
from flask import jsonify


class Matches(Resource):

    # @login_required
    def get(self):
        fixtures = db.session.query(Fixtures).all()
        response = []
        for fixture in fixtures:
            response.append(fixture.my_dict())
        return jsonify(response)
