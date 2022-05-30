from flask_restful import Api

from api.views.authentication import Register, Login
from api.views.templates import TemplatesListCreateAPI, TemplatesListUpdateDeleteAPI


def create_routes(api: Api):
    """Adds resources to the api.
    :param api: Flask-RESTful Api Object
    """
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(TemplatesListCreateAPI, '/template')
    api.add_resource(TemplatesListUpdateDeleteAPI, '/template/<template_id>')
    return api
