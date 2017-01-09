from settings import *

DEBUG = False

IP = '154.117.8.18'
ALLOWED_HOSTS = [IP]

# APIs

# vends
VENDOR_URL = 'http://' + IP + ':8070'
VENDOR_VENDS_URL = VENDOR_URL + '/vends'

# messaging
MESSAGING_URL = 'http://' + IP + ':7710'
TO = [
    'alwaysdeone@gmail.com',
    'georged@spectrawireless.com',
    'sdarko@spectrawireless.com',
    'cadzisu@spectrawireless.com'
]