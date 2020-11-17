from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'fq48sdsdf3ctwn83ynuj4wexe7tb132ctyjn4rs5ehr1cth175n3sr'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
