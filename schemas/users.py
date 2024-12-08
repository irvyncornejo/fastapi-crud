def user_entity(user) -> dict:
    return {
        'id': str(user['_id']),
        'full_name': user['full_name'],
        'email': user['email'],
        'role': user['role'],
        'data': user.get('data', {})
    }

def users_entity(users) -> list:
    return [user_entity(user) for user in users]
