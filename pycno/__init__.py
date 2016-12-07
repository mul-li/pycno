import os
import os.path
import base64

from flask import Flask

from mulli import HexConverter

from .highlight import HighlightExtension

import pkg_resources

config_file = os.path.abspath('config.json')


def create_app():

    app = Flask(__name__)

    try:
        app.config.from_json(config_file)
    except FileNotFoundError:
        pass

    _default_secret_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', _default_secret_key)
    app.config.setdefault('PYCNO_SITE_TITLE', 'Pycno')

    app.url_map.converters['hex'] = HexConverter
    app.jinja_env.add_extension(HighlightExtension)

    from .views import root_page
    app.register_blueprint(root_page)

    @app.context_processor
    def inject_version():
        return dict(PYCNO_VERSION=pkg_resources.require('PYCNO')[0].version)

    return app


app = create_app()
