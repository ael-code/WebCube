import urllib2
from webcube import WebCube

host="192.168.1.1"
username="admin"
password="admin0"

handler=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

wc = WebCube(host, username, password)
print(wc.get_cellular_duration())
wc.login()
#wc.connect()
wc.logout()
