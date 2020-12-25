from mms.datastore_handler import Datastore
from google.cloud import datastore
import uuid

import config

client = Datastore(project_id=config.PROJECT_ID)
ds_handler = datastore.Client(project=config.PROJECT_ID)


def put_new_entity(text, uri, link, kw, isTM):
    try:
        name_id = str(uuid.uuid4())
        task_key = ds_handler.key(config.RECIPE_KIND, name=name_id)
        entity = datastore.Entity(key=task_key, exclude_from_indexes=["textfield"])
        prop_df = {
            'textfield': text,
            'uri': uri,
            'link': link,
            'keywords': kw,
            'isTM': isTM
        }
        for i in prop_df:
            entity[i] = prop_df[i]
        ds_handler.put(entity)
        return None
    except Exception as exc:
        return "DB error: {}".format(exc)


# def save_recipe(text, uri, link, kw, isTM):
#     try:
#         prop_df = {
#             'textfield': text,
#             'uri': uri,
#             'link': link,
#             'keywords': kw,
#             'isTM': isTM
#         }
#         client.put_new_entity(kind=config.RECIPE_KIND, prop_df=prop_df, name=str(uuid.uuid4()))
#         return None
#     except Exception as exc:
#         return "DB error: {}".format(exc)


def get_recipes():
    try:
        result_list = []
        result = client.get_all_of_a_kind(config.RECIPE_KIND)
        for record in result:
            result_list.append({
                "id": record.get('_id'),
                "link": record.get('link'),
                "isTM": record.get('isTM'),
                "keywords": record.get('keywords'),
                "textfield": record.get('textfield')
            })
        return None, result_list
    except Exception as exc:
        return "DB error: {}".format(exc), None


def create_user(user_form):
    try:
        _id = str(uuid.uuid4())
        user_form['user_id'] = _id
        client.put_new_entity(kind=config.USER_KIND, prop_df=user_form)
        # RETURN NEW USER
        user = client.query(kind=config.USER_KIND, filter=["user_id", "=", _id])
        profile = {
            "email": user[0].get('email'),
            "first_name": user[0].get('first_name'),
            "last_name": user[0].get('last_name'),
            "favourites": user[0].get('favourites')
        }
        return None, 200, profile
    except Exception as exc:
        return "DB error: {}".format(exc), 503, None


def get_user(email):
    try:
        f = ["email", "=", email]
        user = client.query(kind=config.USER_KIND, filter=f)
        if len(user) > 0:
            return None, 200, user[0]
        return 'Incorrect email or password entered', 401, None
    except Exception as exc:
        return "DB error: {}".format(exc), 503, None


def update_user_entity(email, data):
    try:
        error, code, user_prop = get_user(email=email)
        if error:
            return error, 503, None
        with ds_handler.transaction():
            user = ds_handler.get(user_prop.key)
            for key, value in data.items():
                user[key] = value
            ds_handler.put(user)
        return None, 200, user_prop
    except Exception as exc:
        return "DB error: {}".format(exc), 503, None


if __name__ == '__main__':
    update_user_entity(email="dominik.schimmer@gmail.com", favourites=['6c176b38-e3fe-4f65-abf6-35d8decfec4f',
                                                                       '9d23260a-29f8-4c0d-8710-dd581c8e8e2f',
                                                                       'ad1d107d-7352-4fe7-8905-084e03077cd0'])