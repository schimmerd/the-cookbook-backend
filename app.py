import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.api.v1.DetectText import AddRecipe
from src.api.v1.GetAllRecipes import Recipes
from src.api.v1.Login import SignIn
from src.api.v1.SignUp import SignUp
from src.api.v1.Update import UpdateUser
from mms.logger.cloud_run_logger import CloudRunLogger

import config

# Init Flask:
# UPLOAD_FOLDER = '/upload'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)

# Create Logger:
logger = CloudRunLogger(project_id=config.PROJECT_ID,
                        local_run=True) # Todo Change in 'cloud' mode


api.add_resource(AddRecipe, "/api/v1/add", resource_class_args=(logger,))
api.add_resource(Recipes, '/api/v1/recipes', resource_class_args=(logger,))
api.add_resource(SignIn, '/api/v1/login', resource_class_args=(logger,))
api.add_resource(SignUp, '/api/v1/signUp', resource_class_args=(logger,))
api.add_resource(UpdateUser, '/api/v1/update', resource_class_args=(logger,))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=int(os.environ.get('PORT', 8080)))
