'''
WebCube keepalive script

It monitors the status of the WebCube and
does everting possible to keep the connection up with the operator.
'''

import urllib2
import logging
import os
import webcube


logging.basicConfig(level=logging.DEBUG)

host = os.environ['WEBCUBE_HOST']
username = os.environ['WEBCUBE_USERNAME']
password = os.environ['WEBCUBE_PASSWORD']

'''
handler=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)
'''

wc = webcube.WebCube(host, username, password)

wan_status = wc.get_wan_status()
logging.debug('wan status: {}'.format(wan_status))
conn_uptime_sec = wc.get_cellular_duration()
logging.debug('conn uptime: {}:{}:{}'.format(conn_uptime_sec/3600, (conn_uptime_sec/60)%60, conn_uptime_sec%60))

if ( wc.get_wan_status() is webcube.DISCONNECTED ) or ( conn_uptime_sec > 3*3600):
    logging.info('Forcing reconnection...')
    with wc.session():
        wc.connect()
