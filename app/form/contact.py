from wtforms import fields, validators

from .csrf import SessionCSRFForm


class ContactForm(SessionCSRFForm):
    name = fields.StringField(
        'Контактное лицо',
        validators=[validators.DataRequired()]
    )

    email = fields.StringField(
        'Электронный адрес',
        validators=[validators.DataRequired(),
                    validators.Email()]
    )

    phone = fields.StringField(
        'Телефон'
    )

    subject = fields.StringField(
        'Тема'
    )

    message = fields.TextAreaField(
        'Сообщение',
        validators=[validators.DataRequired()]
    )
