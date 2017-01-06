from settings import *

IP = '154.117.8.19'
ALLOWED_HOSTS = [IP]

# APIs

# vends
VENDOR_URL = 'http://' + IP + ':8070'
VENDOR_VENDS_URL = VENDOR_URL + '/vends'

# messaging
MESSAGING_URL = 'http://' + IP + ':7710'
TO = ['alwaysdeone@gmail.com']
DEFAULT_FROM_EMAIL = 'Spectra Reporter<incisiaappmailer@gmail.com>'
EMAIL_SUBJECT_AND_BODY = {
    'vends': {
        'subject': 'Vend Report',
        'body': 'Hello,\n\nPlease find vend report attached.\n\nRegards.'
    }
}