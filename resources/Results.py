# # user_betting_history = db.session.query(UserBettingHistory).filter(UserBettingHistory.user_id == user.id,
# #                                                                    UserBettingHistory.fixture_id == fixture_id)
#
#
# from flask_restful import Resource
# from models import *
# from flask import jsonify
# import models
# from flask import request
# from sqlalchemy import or_
#
#
# class Results(Resource):
#
#     def post(self):
#         if hasattr(request, 'authorization'):
#             password = request.headers["authorization"]
#             user = db.session.query(Users).filter(Users.password == password).first()
#             fixture_id = request.values["fixture_id"]
#             team_id = request.values["team_id"]
#             amount = request.values["amount"]
#             bet = db.session.query(models.Bets).filter(models.Bets.user_id == user.id,
#                                                        models.Bets.fixture_id == fixture_id).first()
#             if bet is None:
#                 try:
#                     match_exists = db.session.query(Fixtures).filter(Fixtures.id == fixture_id,
#                                                                      or_(Fixtures.home_team_id == team_id,
#                                                                          Fixtures.away_team_id == team_id)).first()
#                     if match_exists is not None:
#                         new_bet = Bets(user_id=user["id"], fixture_id=fixture_id, amount=amount, team_id=team_id)
#                         db.session.add(new_bet)
#                         db.session.commit()
#                         return jsonify({"Message": "Bet Placed Successfully", "Status-Code": 200})
#                     else:
#                         return "Invalid Request"
#                 except Exception as ex:
#                     return ex.message, 500
#             else:
#                 return "Bet has been already placed, Please update the existing bet."
