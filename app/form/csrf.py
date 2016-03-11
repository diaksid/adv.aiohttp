from wtforms import Form
from wtforms.csrf.session import SessionCSRF

from ..config import session_key


class SessionCSRFForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = session_key

    def __init__(self, session, *args, **kwargs):
        kwargs['meta'] = dict(csrf_context=session)
        super(SessionCSRFForm, self).__init__(*args, **kwargs)
