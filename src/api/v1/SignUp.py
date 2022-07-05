from flask_restful import Resource
from flask import jsonify, request
from src.modules.core.user import sign_up
from src.modules.helper import decode_data


class SignUp(Resource):
    def __init__(self, logger):
        self.logger = logger

    def post(self):
        try:
            error, data = decode_data(req=request.data)
            error, code, profile = sign_up(email=data.get('email'), password=data.get('password'),
                                           first_name=data.get('firstName'), last_name=data.get('lastName'))
            if error:
                self.logger.error(error)
                return error, code
            return jsonify(profile)
        except Exception as exc:
            self.logger.error(str(exc))
            return str(exc), 503
