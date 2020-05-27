from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from evaluator import evaluator_blueprint

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.register_blueprint(evaluator_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
