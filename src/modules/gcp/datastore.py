import os

from google.cloud.datastore import Entity, Client

import uuid


client = Client(project=os.environ.get('GCP_PROJECT_ID'))

recipe_kind = os.environ.get('RECIPE_KIND', 'recipe_lookup')
user_kind = os.environ.get('USER_KIND', 'recipe_user')


def get_recipes():
    try:
        results = []
        query = client.query(kind=recipe_kind)
        result = list(query.fetch())
        for record in result:
            results.append({
                "id": record.get('_id', "n/a"),
                "link": record.get('link', "n/a"),
                "isTM": record.get('isTM', "n/a"),
                "keywords": record.get('keywords', "n/a"),
                "textfield": record.get('textfield', "n/a")
            })
        return None, results
    except Exception as exc:
        return "DB error: {}".format(exc), None


def create_new_recipe(text, uri, link, kw, isTM):
    try:
        name_id = str(uuid.uuid4())
        task_key = client.key(recipe_kind, name=name_id)
        entity = Entity(key=task_key, exclude_from_indexes=("textfield",))
        prop_df = {
            'textfield': text,
            'uri': uri,
            'link': link,
            'keywords': kw,
            'isTM': isTM
        }
        for i in prop_df:
            entity[i] = prop_df[i]
        client.put(entity)
        return None
    except Exception as exc:
        return "DB error: {}".format(exc)


def create_user(user_form):
    try:
        # CREATE USER
        _id = str(uuid.uuid4())
        user_form['user_id'] = _id
        task_key = client.key(kind=user_kind)
        entity = Entity(key=task_key, exclude_from_indexes=())
        for i in user_form:
            entity[i] = user_form[i]
        client.put(entity)

        # RETURN NEW USER
        user = client.query(kind=user_kind, filter=["user_id", "=", _id])
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
        filters = [("email", "=", email)]
        query = client.query(kind=user_kind, filters=filters)
        result = list(query.fetch())
        if len(result) > 0:
            return None, 200, result[0]
        return 'Incorrect email or password entered', 401, None
    except Exception as exc:
        return "DB error: {}".format(exc), 503, None


def update_user_entity(email, data):
    try:
        error, code, user_prop = get_user(email=email)
        if error:
            return error, 503, None
        with client.transaction():
            user = client.get(user_prop.key)
            for key, value in data.items():
                user[key] = value
            client.put(user)
        return None, 200, user_prop
    except Exception as exc:
        return "DB error: {}".format(exc), 503, None


if __name__ == '__main__':
    os.environ.setdefault("USER_KIND", "recipe_user")
    os.environ.setdefault("RECIPE_KIND", "recipe_lookup")
    print(get_user(email="dominik.schimmer@gmail.com"))
    # print(create_new_recipe(text="beispiel text", kw="zb", uri="bucketURL", link="storageLINK", isTM=False))
    # print(get_recipes())
    # update_user_entity(email="dominik.schimmer@gmail.com", favourites=['6c176b38-e3fe-4f65-abf6-35d8decfec4f',
    #                                                                    '9d23260a-29f8-4c0d-8710-dd581c8e8e2f',
    #                                                                    'ad1d107d-7352-4fe7-8905-084e03077cd0'])