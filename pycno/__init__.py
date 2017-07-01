import os
import os.path
import base64

from flask import Flask

from celery import Celery

import pkg_resources

from mulli import Mulli
from mulli import Celery as CeleryExt

from .highlight import HighlightExtension

config_file = os.path.abspath('config.json')

celery = Celery(__name__)

celery_ext = CeleryExt()
mulli_ext = Mulli(hex_converter=True)


def create_app():

    app = Flask(__name__)

    try:
        app.config.from_json(config_file)
    except FileNotFoundError:
        pass

    _default_secret_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', _default_secret_key)

    app.config['SITE_TITLE'] = app.config.get('PYCNO_SITE_TITLE', 'Pycno')
    app.config['ONION_ADDRESS'] = app.config.get('PYCNO_ONION_ADDRESS', None)
    app.config['DATABASE'] = app.config.get('PYCNO_DATABASE', 'pycno.pickle')

    app.config.setdefault('PYCNO_CELERY_BROKER_URL', 'pyamqp://pycno:pycno@localhost:5672/pycno')
    celery_config = app.config.get_namespace('PYCNO_CELERY_', lowercase=False)
    celery_ext.init_app(app, celery_config)

    mulli_ext.init_app(app)

    app.jinja_env.add_extension(HighlightExtension)

    from .views import root_page
    app.register_blueprint(root_page)

    @app.context_processor
    def inject_version():
        return dict(APP_VERSION=pkg_resources.require('pycno')[0].version)

    @app.context_processor
    def inject_index_title():
        return dict(INDEX_TITLE='Paste it!')

    return app


app = create_app()
