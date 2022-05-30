from uuid import uuid4

from flask_jwt_extended import create_access_token
from flask_restful import reqparse

from api.configparser import getTokenExpirationTime
from models.user import User


def get_required(arg, required):
    return True if arg in required else False


def parse_args(args_tuple: tuple = (), required_fields: tuple = ()) -> dict:
    """
    Parses the arguments of a request and performs necessary 
    validation on the required fields, excludes fields not in ``args_tuple``.
    
    :``args_tuple``: tuple of strings containing expected arguments
    
    :``required_fields``: tuple of strings referencing non-nullable ``ODM`` model fields
    """
    parser = reqparse.RequestParser()
    for arg in args_tuple:
        is_required = get_required(arg, required_fields)
        help_message = F'{arg.capitalize()} field is required' if is_required else None
        parser.add_argument(
            arg, type=str, required=is_required, help=help_message)
    args = parser.parse_args()
    args_dict = args.items()
    return {k: v for k, v in args_dict if v}


def generate_tokens(user: User) -> dict:
    """
    Generates JWT tokens for given user.
    :param user: User object
    :return: dict
    """
    access_token = create_access_token(
        identity=user.user_id, expires_delta=getTokenExpirationTime())
    return {'access_token': access_token, 'user': user.full_name}


def generate_user_UUID() -> str:
    """ Generates a universal unique identifier string representing the user's ID. """
    return uuid4()
