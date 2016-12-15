from flask import Blueprint, render_template, redirect, url_for, make_response, abort

import mulli

from . import forms
from . import utils

root_page = Blueprint('root', __name__)


@root_page.route('/', methods=('GET', 'POST'))
def index():
    form = forms.PasteForm()

    if form.validate_on_submit():
        try:
            paste_id = mulli.create_id(form.text.data)
        except ValueError:
            abort(500)

        try:
            utils.save_paste(paste_id, form.text.data)
        except RuntimeError:
            abort(500)

        return redirect(url_for('root.show_paste', paste_id=paste_id))

    return render_template('index.html', form=form)


@root_page.route('/advanced', methods=('GET', 'POST'))
def advanced():
    form = forms.ExtendedPasteForm()

    if form.validate_on_submit():
        try:
            paste_id = mulli.create_id(form.text.data)
        except ValueError:
            abort(500)

        try:
            utils.save_paste(paste_id, form.text.data, form.validity.data, form.syntax.data)
        except RuntimeError:
            abort(500)

        return redirect(url_for('root.show_paste', paste_id=paste_id))

    return render_template('advanced.html', form=form)


@root_page.route('/<hex:paste_id>')
def show_paste(paste_id):
    try:
        paste = mulli.load_entry(paste_id)
    except KeyError:
        return render_template('not_found.html'), 404
    except ValueError:
        mulli.remove_entry(paste_id)
        return render_template('not_found.html'), 404
    else:
        paste_content = paste['content']
        paste_lexer = paste['lexer']
    return render_template('paste.html', paste_id=paste_id, paste_content=paste_content, paste_lexer=paste_lexer)


@root_page.route('/raw/<hex:paste_id>')
def raw(paste_id):
    try:
        paste = mulli.load_entry(paste_id)
    except KeyError:
        return render_template('not_found.html'), 404
    except ValueError:
        mulli.remove_entry(paste_id)
        return render_template('not_found.html'), 404
    else:
        paste_content = paste['content']
    response = make_response(paste_content)
    response.mimetype = 'text/plain'
    return response


@root_page.route('/about')
def about():
    return render_template('about.html')
