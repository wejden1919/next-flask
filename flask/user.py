

def user_is_valid(user):
    required_keys = {'username', 'email', 'password'}  
    user_keys = set(user.keys())  
    return required_keys.issubset(user_keys)