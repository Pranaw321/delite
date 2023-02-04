import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
# from delite import custom_exceptions as exc


def get_token_for_user(user, scope):
    """
    Generate a new signed token containing
    a specified user limited for a scope (identified as a string).
    """
    data = {
        "user_id": str(user.id),
        "phone": str(user.phone),
    }  
     
    return jwt.encode(data, settings.SECRET_KEY,  algorithm="HS256")


def get_user_for_token(request):
    """
    Given a selfcontained token and a scope try to parse and
    unsign it.

    If max_age is specified it checks token expiration.

    If token passes a validation, returns
    a user instance corresponding with user_id stored
    in the incoming token.
    """
    token = request.headers.get('accessToken')
    try:
        data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[ 'HS256'])
        return data
       
    except jwt.DecodeError:
        # raise exc.NotAuthenticated("Invalid token")
        pass

  
    
   
        
       