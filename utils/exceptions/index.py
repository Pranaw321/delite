import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
# from delite import custom_exceptions as exc
# from rest_framework.views import exception_handler


def get_token_for_user(user, scope):
    """
    Generate a new signed token containing
    a specified user limited for a scope (identified as a string).
    """
    data = {
        "user_%s_id" % (scope): str(user.id),
    }
    return jwt.encode(data, settings.SECRET_KEY).decode()


# def get_user_for_token(token, scope):
#     """
#     Given a selfcontained token and a scope try to parse and
#     unsign it.

#     If max_age is specified it checks token expiration.

#     If token passes a validation, returns
#     a user instance corresponding with user_id stored
#     in the incoming token.
#     """
#     try:
#         data = jwt.decode(token, settings.SECRET_KEY)
#     except jwt.DecodeError:
#         raise exc.NotAuthenticated("Invalid token")

#     model_cls = get_user_model()

#     try:
#         user = model_cls.objects.get(pk=data["user_%s_id" % (scope)])
#     except (model_cls.DoesNotExist, KeyError):
#         raise exc.NotAuthenticated("Invalid token")
#     else:
#         return user
   

# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     # Now add the HTTP status code to the response.
#     if response is not None:
#         response.data['status_code'] = response.status_code

#     return response