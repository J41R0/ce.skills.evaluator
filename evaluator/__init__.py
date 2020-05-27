from flask import Blueprint
from flask_restx import Api

from evaluator.api import evaluator_namespace

evaluator_blueprint = Blueprint('evaluator', __name__)

description = """
## Detailed description  \n
The evaluation service provide a way to define how good is an engineer using the data stored on Cuban Engineer platform

The current used providers are:
\n* GitHub
\n* GitLab
\n* Stack Exchange

Any new evaluator must follow the input/output behavior defined in '/evaluate' endpoint. 

### Endpoints  \n
\n* '/evaluate': Default evaluator used by Cuban Engineer platform
\n* '/data_mock': Provide mocked profiles data 
  
### Mocked data
The '/data_mock' endpoint provide a set of anonymous data stored on Cuban Engineer platform

The service purposes are:
\n* Provide a way to test custom evaluation services
\n* Give an estimated evaluation of each engineer to get an idea about how an evaluation service should behave 

In service documentation is provided a sorted result, from higher to lower, of provided profiles with some comments

Note: Any evaluator should return a similar result to presented in documentation 
"""

evaluator_api = Api(evaluator_blueprint, version='1.0', title='Skill Evaluator API',
                    description=description)

evaluator_api.add_namespace(evaluator_namespace, path='/')
