from flask_restful import Resource
from flask import jsonify, request
from src.modules.core.user import update
from src.modules.helper import decode_data


class UpdateUser(Resource):
    def __init__(self, logger):
        self.logger = logger

    def post(self):
        try:
            email = request.args.get('email')
            error, data = decode_data(req=request.data)
            error, code, profile = update(email=email, data=data)
            if error:
                self.logger.error(error)
                return error, code
            return jsonify(profile)
        except Exception as exc:
            self.logger.error(str(exc))
            return str(exc), 503
