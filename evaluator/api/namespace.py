from flask_restx import Namespace

api_namespace = Namespace('Skills evaluator endpoints',
                          description='')


def get_content(api_model):
    @api_namespace.marshal_with(api_model)
    def get_request():
        return api_namespace.payload

    return get_request()
