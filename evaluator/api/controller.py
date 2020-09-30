import http
import json

from flask_restx import Resource

from evaluator.api.namespace import api_namespace
from evaluator.api.dto.profile import ProfilesDto
from evaluator.api.dto.skill import EvaluatedSkillsDto
from evaluator.app.evaluation_service import evaluate_skills


@api_namespace.route('evaluate')
class Evaluator(Resource):

    @api_namespace.marshal_with(EvaluatedSkillsDto.skill_list)
    @api_namespace.expect(ProfilesDto.profile_list, validate=True)
    def post(self):
        """Evaluate engineers according to profiles data using an smart evaluation process with skills inference
        ## Description
        Default evaluation service used by Cuban Engineer platform
        Example input data:

        ```
        {
              "profiles": [
                {
                  "provider": "GITHUB",
                  "stats": {
                    "followers": "1"
                  },
                  "repositories": [
                    {
                      "id": 1,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 17,
                      "userCommits": 16,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    },
                    {
                      "id": 2,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 0,
                      "userCommits": 1,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    },
                    {
                      "id": 3,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 0,
                      "userCommits": 1,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    },
                    {
                      "id": 4,
                      "isFork": true,
                      "contributors": 0,
                      "totalCommits": 0,
                      "userCommits": 0,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    }
                  ],
                  "skills": [
                    {
                      "repositoryId": 1,
                      "name": "Java",
                      "value": 6329.0
                    },
                    {
                      "repositoryId": 3,
                      "name": "Java",
                      "value": 2053.0
                    }
                  ]
                },
                {
                  "provider": "GITLAB",
                  "stats": {},
                  "repositories": [
                    {
                      "id": 1,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 16,
                      "userCommits": 16,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 5,
                      "totalAdditions": 15
                    }
                  ],
                  "skills": [
                    {
                      "repositoryId": 1,
                      "name": "Java",
                      "value": 6544487.0
                    }
                  ]
                }
          ],
          "scaleLowerBound": 1,
          "scaleHigherBound": 10
        }
        """
        profiles_data = ProfilesDto()
        evaluated_skills = evaluate_skills(profiles_data.profiles,
                                           profiles_data.scale_lower_bound,
                                           profiles_data.scale_higher_bound,
                                           profiles_data.infer_skills)
        skills_json = EvaluatedSkillsDto.build_json_from_skills(evaluated_skills)
        return skills_json, http.HTTPStatus.OK


@api_namespace.route('naive_evaluate')
class NaiveEvaluator(Resource):

    @api_namespace.marshal_with(EvaluatedSkillsDto.skill_list)
    @api_namespace.expect(ProfilesDto.profile_list, validate=True)
    def post(self):
        """Evaluate engineers according to profiles data
        ## Description
        Evaluation service used by Cuban Engineer platform
        Example input data:

        ```
        {
              "profiles": [
                {
                  "provider": "GITHUB",
                  "stats": {
                    "followers": "1"
                  },
                  "repositories": [
                    {
                      "id": 1,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 17,
                      "userCommits": 16,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    },
                    {
                      "id": 2,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 0,
                      "userCommits": 1,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    },
                    {
                      "id": 3,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 0,
                      "userCommits": 1,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    },
                    {
                      "id": 4,
                      "isFork": true,
                      "contributors": 0,
                      "totalCommits": 0,
                      "userCommits": 0,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 0,
                      "totalAdditions": 0
                    }
                  ],
                  "skills": [
                    {
                      "repositoryId": 1,
                      "name": "Java",
                      "value": 6329.0
                    },
                    {
                      "repositoryId": 3,
                      "name": "Java",
                      "value": 2053.0
                    }
                  ]
                },
                {
                  "provider": "GITLAB",
                  "stats": {},
                  "repositories": [
                    {
                      "id": 1,
                      "isFork": false,
                      "contributors": 0,
                      "totalCommits": 16,
                      "userCommits": 16,
                      "forks": 0,
                      "stars": 0,
                      "views": 0,
                      "userAdditions": 5,
                      "totalAdditions": 15
                    }
                  ],
                  "skills": [
                    {
                      "repositoryId": 1,
                      "name": "Java",
                      "value": 6544487.0
                    }
                  ]
                }
          ],
          "scaleLowerBound": 1,
          "scaleHigherBound": 10
        }
        """
        profiles_data = ProfilesDto()
        evaluated_skills = evaluate_skills(profiles_data.profiles,
                                           profiles_data.scale_lower_bound,
                                           profiles_data.scale_higher_bound,
                                           custom_evaluation=False)
        skills_json = EvaluatedSkillsDto.build_json_from_skills(evaluated_skills)
        return skills_json, http.HTTPStatus.OK


@api_namespace.route('data_mock')
class Mock(Resource):

    def get(self):
        """Anonymous profiles mock to test custom evaluation services
        ## Preliminary profiles evaluation rank
        \n1. Goofy: Experienced developer with knowledge in several technologies, but manly frontend skills
        \n2. Woody: Good backend developer with knowledge in several languages and frameworks, also with frontend skills
        \n3. Pumba: Good python developer, with web development experience
        \n4. Pluto: Strong frontend developer
        \n5. Mickey: Strong frontend developer
        \n6. Baloo: Regular frontend developer
        \n7. Timon: Regular frontend developer
        \n8. Mushu: Regular Java developer
        \n9. Minie: Regular Java developer
        \n10. Boo: Some Java backned development knowledge
        \n11. Donald: Some Java backned development knowledge
        \n12. Simba: Some c++ knowledge
        \n13. Pooh: Some Python knowledge
        \n14. Aurora: Some Python knowledge

        """
        with open("evaluator/api/resources/mock.json", 'r') as file:
            mock_str = file.read()
        mock_json = json.loads(mock_str)
        return mock_json, http.HTTPStatus.OK
