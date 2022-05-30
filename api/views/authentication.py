from flask import Response, make_response
from flask_restful import Resource, abort
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from utils.utils import generate_tokens, generate_user_UUID, parse_args

from models.user import User


class Register(Resource):
    """ Flask-resftul resource for User creation. """

    def post(self):
        """ Create a new user. """
        fields = ('email', 'password', 'first_name', 'last_name')
        args = parse_args(args_tuple=fields, required_fields=fields)
        user = User(user_id=generate_user_UUID(), email=args['email'], password=args['password'],
                    first_name=args['first_name'], last_name=args['last_name'])
        if user.email_is_unique():
            user = user.save()
            return {'message': 'User created successfully'}, 201
        return {'message': 'Email address already exists'}, 400


class Login(Resource):
    """ Flask-resftul resource for retrieving user web token. """

    def post(self) -> Response:
        fields = ('email', 'password')
        data = parse_args(args_tuple=fields, required_fields=fields)
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if not (user and user.verify_password(password=password)):
            return abort(401, message='Invalid username or password')
        return make_response(generate_tokens(user), 200)
