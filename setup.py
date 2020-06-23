import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Skill-Evaluator',
    version='1.0',
    scripts=[],
    author="Cuban engineer",
    author_email="contact@cuban.engineer",
    description="Default skill evaluator project for cuban engineer plataform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'gunicorn >= 20.0.4',
        'werkzeug >= 0.15.4',
        'flask-restx >= 0.2.0',
        'flask_cors >= 3.0.7',
        'flask_jwt_extended >= 3.10.0',
        'coverage >= 5.1',
        'Py-FCM >= 0.2.21'
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
