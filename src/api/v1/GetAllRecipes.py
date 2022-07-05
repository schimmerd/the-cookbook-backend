from flask_restful import Resource
from flask import jsonify
from src.modules.core.recipe import get_all_recipes


class Recipes(Resource):
    def __init__(self, logger):
        self.logger = logger

    def get(self):
        try:
            error, recipe_list = get_all_recipes()
            if error:
                self.logger.error(error)
                return error, 503
            return jsonify(recipe_list)
        except Exception as exc:
            self.logger.error(str(exc))
            return str(exc), 503
