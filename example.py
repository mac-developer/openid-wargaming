"""Example to test library."""


import re
import _thread
from http.server import BaseHTTPRequestHandler, HTTPServer

from openid_wargaming.authentication import Authentication
from openid_wargaming.verification import Verification

VERIFY_URL = ''
PORT=8000

class SimpleHTTP(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global VERIFY_URL
        def killme(server):
            server.shutdown()
        
        self._set_response()
        VERIFY_URL = self.path
        self.wfile.write(b'Success! Check your console ...')
        _thread.start_new_thread(killme, (self.server,))





return_to = 'http://localhost:8000/'
auth = Authentication(return_to=return_to)

url = auth.authenticate('https://eu.wargaming.net/id/openid/')
print('''
##################
# Open this url: #
------------------
{0}
------------------
'''.format(url))

httpd = HTTPServer(('', PORT), SimpleHTTP)
httpd.serve_forever()

current_url = '{0}{1}'.format(return_to.rstrip('/'), VERIFY_URL)
regex = r'https://eu.wargaming.net/id/([0-9]+)-(\w+)/'

verify = Verification(current_url)
identities = verify.verify()

match = re.search(regex, identities['identity'])
account_id = match.group(1)
nickname = match.group(2)

print('''
### Wargaming nickname authenticated: {0}'''.format(nickname))