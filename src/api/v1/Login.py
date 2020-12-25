from flask_restful import Resource
from flask import jsonify, request
from src.modules.helper import login, decode_data


class SignIn(Resource):
    def __init__(self, logger):
        self.logger = logger

    def post(self):
        try:
            error, data = decode_data(req=request.data)
            error, code, profile = login(email=data.get('email'), password=data.get('password'))
            if error:
                self.logger.error(error)
                return error, code
            return jsonify(profile)
        except Exception as exc:
            self.logger.error(str(exc))
            return str(exc), 503