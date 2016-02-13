import urllib2
import urllib
import xml.etree.ElementTree as ET

host="192.168.1.1"
user="admin"
password="admin"

handler=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

def get_cellular_duration():
    data = "<request><wan></wan></request>"
    response = urllib2.urlopen('http://{}/api/status'.format(host), data)
    duration = int(ET.fromstring(response.read()).find("cellular_duration").text)
    print(duration)

def login(user, password):
    user = urllib.quote(user)
    password = urllib.quote(password)
    data = "<request><Username>{}</Username><Password>{}</Password></request>".format(user,password)
    response = urllib2.urlopen('http://{}/api/login'.format(host), data)
    code = ET.fromstring(response.read()).text.split(",")
    if (code != ['0', '0']):
        if (code == ['2','0']):
            raise Exception("Another user is logged in")
        elif (code == ['3','0']):
            raise Exception("Too many attempts, retry later (1 minute)")
        else:
            raise Exception("Unknown error code: {},{}".format(code[0],code[1]))
    set_cookie = response.info().getheader("Set-Cookie").split(";",1)
    sessionID = set_cookie[0]
    return sessionID

def reboot(sessionID):
    data = "<request>1</request>"
    header = {"Cookie": sessionID}
    req = urllib2.Request('http://{}/apply.cgi'.format(host), "CMD=reboot", header)
    response = urllib2.urlopen(req)

def logout(sessionID):
    data = "<request>1</request>"
    header = {"Cookie": sessionID}
    req = urllib2.Request('http://{}/api/logout'.format(host), data, header)
    response = urllib2.urlopen(req)
    code = ET.fromstring(response.read()).text
    if code != "OK":
        raise Exception("Error while logging out")

get_cellular_duration()
sessionID = login(user, password)
#reboot(sessionID)
logout(sessionID)

