from datetime import datetime
from src.modules.gcp.push_to_pubsub import upload
from src.modules.gcp.datastore import put_new_entity, get_recipes, get_user, create_user, update_user_entity
from google.cloud import vision
import bcrypt
import pytz
import json
import uuid

import config


def get_time(time_zone='UTC'):
    """
    Creating a timestamp object
    Args:
     time_zone: UTC
    Returns:
        current timestamp
    """
    tz = pytz.timezone(time_zone)
    return datetime.now(tz)


def get_uuid():
    """
    Creating an unique id
    Returns: str, uuid4
    """
    return str(uuid.uuid4())


def decode_data(req):
    """
    Converts the requests_data into a dictionary
    Args:
        req: b'str'
    Returns:
        error: None if no error; str with error message if any error
        data: dict of request_data if no error; None if any error
    """
    try:
        data = json.loads(req.decode('utf-8'))
        return None, data
    except Exception as exc:
        return 'Service unable to decode data: {}'.format(exc), None


def check_is_valid(**kwargs):
    """
    Checks if incoming request is valid (not None)
    Args:
        kwargs: *
    Returns:
        error: None if no error/no invalid request params; str with error message if any error
    """
    try:
        black_list = []
        for key, value in kwargs.items():
            if value is None:
                black_list.append(key)
            if value == "":
                black_list.append(key)
        if len(black_list) > 0:
            return "Following parameters should not be None or empty: {}".format(", ".join(black_list))
        return None
    except Exception as exc:
        return 'Service unable to validate incoming request: {}'.format(exc)


def sign_up(email, password, first_name, last_name):
    try:
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)
        user_form = {
            "email": email,
            "password": hashed_password,
            "first_name": first_name,
            "last_name": last_name
        }
        error, code, user = create_user(user_form=user_form)
        if error:
            return error, code, None
        return None, code, user
    except Exception as exc:
        return 'Service unable to create a new user: {}'.format(exc), 503, None


def login(email, password):
    try:
        error, code, user = get_user(email=email)
        if error:
            return error, code, None
        if bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=user.get('password')):
            del user['password']
            return None, code, user
        return 'Incorrect email or password', 401, None
    except Exception as exc:
        return 'Service unable to authenticate user: {}'.format(exc), 503, None


def update(email, data):
    try:
        error, code, profile = update_user_entity(email=email, data=data)
        if error:
            return error, code, None
        return None, 200, profile
    except Exception as exc:
        return 'Service unable to update user entity: {}'.format(exc), 503, None


def add_new_recipe(kw, isTM, files):
    try:
        if 'files[]' not in files:
            return 'Error: No file part', None
        files = files.getlist('files[]')

        for file in files:
            filename = file.filename
            if file and allowed_file(filename):
                # UPLOAD FILE TO GCS
                error, dest_name = upload(file=file, name=filename)
                if error:
                    return error
                # DETECT TEXT
                url = 'gs://{}/{}'.format(config.BUCKET_NAME, dest_name)
                error, texts = detect_text(uri=url)
                if error:
                    return error
                raw_text = texts[0].description
                # SAVE PARAMS ON DATA STORE
                link = 'https://{}/{}'.format(config.LINK_PREFIX, dest_name)
                # error = save_recipe(text=raw_text, uri=url, link=link, kw=kw, isTM=isTM)
                error = put_new_entity(text=raw_text, uri=url, link=link, kw=kw, isTM=isTM)
                if error:
                    return error
        return None
    except Exception as exc:
        return 'Service unable to check file upload: {}'.format(exc)


def get_all_recipes():
    try:
        error, recipe_list = get_recipes()
        if error:
            return error, None
        return None, recipe_list
    except Exception as exc:
        return 'Service unable to get all recipes: {}'.format(exc), None


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def detect_text(uri):
    try:
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image)
        if response.error.message:
            return response.error.message, None

        text = response.text_annotations
        return None, text
    except Exception as exc:
        return 'Service unable to detect text: {}'.format(exc), None
