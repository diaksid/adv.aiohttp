from wtforms import fields, validators

from .csrf import SessionCSRFForm


class CallbackForm(SessionCSRFForm):
    name = fields.StringField(
        'Контактное лицо',
        validators=[validators.DataRequired()]
    )

    phone = fields.StringField(
        'Телефон',
        validators=[validators.DataRequired()]
    )
