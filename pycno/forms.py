from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired

from pygments.lexers import get_all_lexers


all_lexers = [(short_names[0], name) for name, short_names, _, _ in get_all_lexers()]
all_lexers.sort(key=lambda x: x[0])


class PasteForm(FlaskForm):

    text = TextAreaField('Text', validators=[InputRequired('This field is required!')])
    submit = SubmitField('Paste it!')


class ExtendedPasteForm(PasteForm):

    validity = SelectField(
        'Validity',
        validators=[InputRequired()],
        choices=[
            ('1', '1 Day'),
            ('7', '1 Week'),
            ('30', '30 Days'),
            ('365', '1 Year'),
        ],
        default='30'
    )

    syntax = SelectField(
        'Syntax',
        validators=[InputRequired()],
        choices=all_lexers
    )
