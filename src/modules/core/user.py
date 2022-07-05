from src.modules.gcp.datastore import create_user, get_user, update_user_entity
import bcrypt


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