from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'pwd')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    # Use get instead of [username] so that we can set a default value of None
    user = username_mapping.get(username, None)
    # Don't compare with == because of different formats
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
