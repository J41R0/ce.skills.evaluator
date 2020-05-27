# Skills evaluator service

Default skill evaluator project for cuban engineer plataform

## Install and run the application 

1. Create python virtual environment and activate it:

    ```
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    ```
2. Clone repository:
    ```
    (venv) $ git clone git@gitlab.com:aleph-engineering/skills-evaluator.git
    (venv) $ cd skills-evaluator
    ```
3. Install setup tools:
    ```
    (venv) $ pip install setuptools
    ```
4. Install dependencies:
    ```
    (venv) $ python setup.py install
    ```
5. Run application:
    ```
    (venv) $ gunicorn --bind 0.0.0.0:5000 --reload wsgi:app
    ```

6. Run tests:
    ```
    (venv) $ cd tests
    (venv) $ python -m unittest discover .
    ```