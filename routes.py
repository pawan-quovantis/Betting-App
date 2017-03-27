from server import app
from resources import Matches, Bets, Users, BettingHistory, Teams
from flask_restful import Api

api = Api(app)
api.add_resource(Matches, '/matches')
api.add_resource(Bets, '/bets')
api.add_resource(Users, '/users')
api.add_resource(BettingHistory, '/betting-history')
api.add_resource(Teams, '/teams')
