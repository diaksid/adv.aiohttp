from smtplib import SMTP, SMTP_SSL, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr, make_msgid

from aiohttp_jinja2 import render_string

from ..config import mail as config


def _subject(subject):
    try:
        subject.encode('ascii')
    except UnicodeEncodeError:
        subject = Header(subject, 'utf-8').encode()
    return subject


def _address(address):
    if isinstance(address, str):
        address = parseaddr(address)
    name, email = address
    name = Header(name, 'utf-8').encode()
    try:
        email.encode('ascii')
    except UnicodeEncodeError:
        if '@' in email:
            box, domain = email.split('@', 1)
            box = str(Header(box, 'utf-8'))
            domain = domain.encode('idna').decode('ascii')
            email = '@'.join((box, domain,))
        else:
            email = Header(email, 'utf-8').encode()
    return formataddr((name, email,))


def _addresses(addresses):
    if isinstance(addresses, str):
        addresses = [addresses]
    return map(lambda a: _address(a), addresses)


class EmailMultipart(object):
    def __init__(self, request):
        self.request = request
        self.msg = MIMEMultipart('alternative')
        self.address = _address(config['address'])
        self.recipients = list(_addresses(config['recipients']))
        self.msg['To'] = ', '.join(self.recipients)
        self.msg['Message-ID'] = make_msgid()

    def contact(self, data):
        self.msg['From'] = _address((data['name'], data['email'],))
        self.msg['Reply-To'] = self.msg['Sender'] = self.msg['From']
        self.msg['Subject'] = _subject(
            '%s: %s' % (config['prefix'],
                        data.get('subject', None) or 'сообщение',))
        self.msg.attach(MIMEText(render_string(
            'mail/plain/contact.html', self.request, data), 'plain'))
        self.msg.attach(MIMEText(render_string(
            'mail/html/contact.html', self.request, data), 'html'))

    def callback(self, data):
        self.msg['From'] = self.msg['Sender'] = self.address
        self.msg['Subject'] = _subject(
            '%s: обратный звонок' % config['prefix'])
        self.msg.attach(MIMEText(render_string(
            'mail/plain/callback.html', self.request, data), 'plain'))
        self.msg.attach(MIMEText(render_string(
            'mail/html/callback.html', self.request, data), 'html'))

    async def send(self, debug=False):
        if config['ssl']:
            smtp = SMTP_SSL(*config['server'])
        else:
            smtp = SMTP(*config['server'])
        smtp.set_debuglevel(debug)
        smtp.login(*config['user'])
        try:
            smtp.sendmail(self.address, self.recipients, self.msg.as_string())
            smtp.quit()
        except SMTPException:
            if not debug:
                raise
            return False
        else:
            return True
