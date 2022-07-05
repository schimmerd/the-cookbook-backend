from flask_restful import Resource
from flask import request
from src.modules.core.recipe import add_new_recipe
from src.modules.helper import check_is_valid


class AddRecipe(Resource):
    def __init__(self, logger):
        self.logger = logger

    def post(self):
        try:
            # GET FORM DATA
            keyword = request.form.get('keywords')
            isTM = request.form.get('isTM')
            # GET FILES
            files = request.files
            error = check_is_valid(keyword=keyword, isTm=isTM)
            if error:
                self.logger.error(error)
                return error, 400
            error = add_new_recipe(kw=keyword, isTM=isTM, files=files)
            if error:
                self.logger.error(error)
                return error, 503
            return 'ok', 200
        except Exception as exc:
            self.logger.error(str(exc))
            return str(exc), 503
