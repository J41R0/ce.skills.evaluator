from flask_restx import fields

from evaluator.api.namespace import api_namespace


class EvaluatedSkillsDto:
    user_skill = api_namespace.model('evaluated_skill', {
        'name': fields.String(required=True, description='profile name'),
        'final_evaluation': fields.Float(required=True, description='final skill evaluation'),
        'scores': fields.Raw(required=True, description='map shaped { -skill_name- : -value-}')
    })

    skill_list = api_namespace.model('skill_list', {
        'skills': fields.List(fields.Nested(user_skill), required=True,
                              description='list of profiles')
    })

    @staticmethod
    def build_json_from_skills(evaluated_skills):
        response = []
        skill_data = evaluated_skills.get_skills_data()
        for skill in skill_data:
            response.append(skill_data[skill])
        return {'skills': response}
