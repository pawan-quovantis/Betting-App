from flask_restful import Api

from resources.teams import Teams
from resources.users import Users
from resources.users import User
from resources.betting_history import BettingHistory
from resources.bets import Bets
from resources.fixtures import Fixtures
from resources.login import Login
from server import app

api = Api(app)
api.add_resource(Fixtures, '/fixtures')
api.add_resource(Bets, '/bets')
api.add_resource(Users, '/users')
api.add_resource(User, '/user')
api.add_resource(BettingHistory, '/betting-history')
api.add_resource(Teams, '/teams')
api.add_resource(Login, '/login')
