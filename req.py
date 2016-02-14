import urllib2
import urllib
import xml.etree.ElementTree as ET

host="192.168.1.1"
username="admin"
password="admin"

handler=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)


class WebCube():

    def __init__(self, host, username=None, password=None):
        self.host = host
        self.username = username
        self.password = password
        self._sessionID = None

    @property
    def url(self):
        return 'http://{}'.format(self.host)

    @property
    def sessionID(self):
        if not self._sessionID:
            raise Exception("You are not currently logged in")
        return self._sessionID

    def get_cellular_duration(self):
        data = "<request><wan></wan></request>"
        response = urllib2.urlopen(self.url + '/api/status', data)
        duration = int(ET.fromstring(response.read()).find("cellular_duration").text)
        return duration

    def login(self):
        if not self.username:
            raise Exception('Could not login: username not set')
        if not self.password:
            raise Exception('Could not login: password not set')
        user = urllib.quote(self.username)
        password = urllib.quote(self.password)
        data = "<request><Username>{}</Username><Password>{}</Password></request>".format(user,password)
        response = urllib2.urlopen(self.url + '/api/login', data)
        code = ET.fromstring(response.read()).text
        if (code != '0,0'):
            if (code == '2,0'):
                raise Exception("Another user is logged in")
            elif (code == '3,0'):
                raise Exception("Too many attempts, retry later (1 minute)")
            elif(code == '1,1'):
                raise Exception("Wrong attempt number one")
            elif(code == '1,2'):
                raise Exception("Wrong attempt number two")
            else:
                raise Exception("Unknown error code: '{}'".format(code))
        set_cookie = response.info().getheader("Set-Cookie").split(";",1)
        self._sessionID = set_cookie[0]

    def logout(self):
        data = "<request>1</request>"
        header = {"Cookie": self.sessionID}
        req = urllib2.Request(self.url + '/api/logout', data, header)
        response = urllib2.urlopen(req)
        code = ET.fromstring(response.read()).text
        if code != "OK":
            raise Exception("Error while logging out")
        self._sessionID = None

    def connect(self):
        data = "<request></request>"
        header = {"Cookie": self.sessionID}
        req = urllib2.Request(self.url + '/api/generic/connect', data, header)
        response = urllib2.urlopen(req)
        try:
            code = ET.fromstring(response.read()).text
        except ET.ParseError:
            raise Exception("Could not parse response as xml")
        if code != "OK":
            raise Exception("Response was not positive")

    def reboot(self):
        data = "<request>1</request>"
        header = {"Cookie": self.sessionID}
        req = urllib2.Request(self.url + '/apply.cgi', "CMD=reboot", header)
        response = urllib2.urlopen(req)



wc = WebCube(host, username, password)
print(wc.get_cellular_duration())
wc.login()
wc.connect()
wc.logout()
