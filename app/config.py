debug = True
test = False

server = ('127.0.0.1', 7220,)

session_key = b'wKLeuG--p702-3jzWvZ_99ngUi4ueJOM'

database = dict(
    auth=False,
    login='admin',
    passw='1234567',
    host=['127.0.0.1:27017'],
    name='cck.ctrl',
)

redis = dict(
    server=('127.0.0.1', 6379,),
    db=0,
)

memcache = dict(
    server=('127.0.0.1', 11211,),
    expire=60 * 60 * 24,
    prefix='cck.ctrl',
)

minify = dict(
    plain=True,
    strict=True,
    code=True,
)

static = '/assets'
media = '/media'

mail = dict(
    address=('СТР.К', 'default@gkcck.ru',),
    recipients=('diaksid@mail.ru',),
    server=('smtp.yandex.ru', 465,),
    user=('default@gkcck.ru', '+1234567',),
    ssl=True,
    prefix='СТР.К',
)

yandex = {'metrika': 35912640,
          'search': {'key': '',
                     'searchid': 0,
                     'login': ''}}
