from flask import Response, jsonify, make_response
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.template import Template

from utils.utils import parse_args


class TemplatesListUpdateDeleteAPI(Resource):
    """ RESTFul API endpoint for Template creation and retrieval. """

    @jwt_required()
    def get(self, template_id: int) -> Response:
        """
        Get a template authored by the requesing user with the given template_id.
        JSON Web Token is required and User must have authored the document.
        """
        template = Template.objects.filter(template_id=template_id).first()
        if not template:
            abort(404, message='Template not found')
        if not template.author_id == get_jwt_identity():
            abort(403, message='You do not have access to this template.')
        return make_response(jsonify(data={'template': template}), 200)

    @jwt_required()
    def put(self, template_id: int) -> Response:
        """
        Updates a template authored by the requesing user with the given template_id.
        JSON Web Token is required and User must have authored the document.
        """
        template = Template.objects.filter(template_id=template_id).first()
        if not template:
            abort(404, message='Template not found')
        if not template.author_id == get_jwt_identity():
            abort(403, message='You do not have access to modify this template.')
        args = parse_args(args_tuple=('template_name', 'subject', 'body'))
        if not args:
            return abort(406, message='At least one valid field is required to process update request.')
        if (template.template_name, template.subject, template.body) == (args['template_name'], args['subject'], args['body']):
            return make_response('', 304)
        template.update(**args)
        template.save()
        return make_response('', 204)

    @jwt_required()
    def delete(self, template_id: int) -> Response:
        """
        Delete a template authored by the requesing user with the given template_id.
        The template is only deleted if the requesting user is the author.
        """
        template = Template.objects.filter(template_id=template_id).first()
        if not template:
            abort(404, message='Template not found')
        if not template.author_id == get_jwt_identity():
            abort(403, message='You do not have access to delete this template.')
        template.delete()
        return make_response('', 204)


class TemplatesListCreateAPI(Resource):
    """ RESTFul API endpoint for Template creation and bulk retrieval. """
    @jwt_required()
    def post(self) -> Response:
        """ Creates a new template for the requesting user. """
        fields = ('template_name', 'subject', 'body')
        parsed_args = parse_args(args_tuple=fields, required_fields=(fields))
        parsed_args.update({'author_id': get_jwt_identity()})
        new_template = Template(**parsed_args)
        new_template = new_template.save()
        if not new_template:
            return abort(400, message='Template could not be created.')
        return make_response({'message': 'Template successfully created'}, 201)

    @jwt_required()
    def get(self) -> Response:
        """
        Get all templates authored by the requesting user.
        The templates are returned in a list.
        """
        templates = Template.objects.filter(author_id=get_jwt_identity())
        if not templates:
            return make_response('', 204)
        return make_response({'templates': templates}, 200)
