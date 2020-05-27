from flask_restx import fields

from evaluator.api.namespace import api_namespace, get_content
from evaluator.domain.profile_objects import Profile


class ProfilesDto:
    respository = api_namespace.model('repository', {
        'id': fields.Integer(required=True, description='repository ID'),
        'isFork': fields.Boolean(required=False, description='forked repository', default=False),
        'contributors': fields.Integer(required=False, description='contributors amount', default=0),
        'forks': fields.Integer(required=False, description='amount of forks done to repository', default=0),
        'stars': fields.Integer(required=False, description='repository stars amount', default=0),
        'views': fields.Integer(required=False, description='views amount', default=0),
        'totalCommits': fields.Integer(required=False, description='repository total commit', default=0),
        'userCommits': fields.Integer(required=False, description='repository user commit', default=0)
    })

    skill = api_namespace.model('skill', {
        'repositoryId': fields.Integer(required=False, description='repository ID', default=0),
        'name': fields.String(required=True, description='skill name'),
        'value': fields.Float(required=True,
                              description='In GITHUB and GITLAB is the amount of bytes of codes')
    })

    profile = api_namespace.model('profile', {
        'provider': fields.String(required=True, description='skills provider'),
        'stats': fields.Raw(required=True, description='...'),
        'repositories': fields.List(fields.Nested(respository), required=True,
                                    description='profile list of repositories'),
        'skills': fields.List(fields.Nested(skill), required=True,
                              description='profile list of skills')
    })

    profile_list = api_namespace.model('profile_list', {
        'profiles': fields.List(fields.Nested(profile), required=True,
                                description='list of profiles'),
        'scale_lower_bound': fields.Integer(required=False, description='output minimum value', default=-1),
        'scale_higher_bound': fields.Integer(required=False, description='output maximum value', default=1)
    })

    def __init__(self):
        input_data = get_content(ProfilesDto.profile_list)
        self.profiles = input_data['profiles']
        self.scale_lower_bound = input_data['scale_lower_bound']
        self.scale_higher_bound = input_data['scale_higher_bound']
