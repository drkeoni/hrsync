#!/usr/bin/env python3
#
# this script is hacked from the original script at https://github.com/orcasgit/python-fitbit
#
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser
import logging
import json

from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError

LOG_FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(LOG_FORMAT))
log.addHandler(ch)

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
AUTH_FILE = os.path.join(ROOT,'.fitbit_auth.json')


class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()

def run():
    try:
        client_id = os.environ['FITBIT_APP_ID']
        client_secret = os.environ['FITBIT_APP_SECRET']
        server = OAuth2Server(client_id, client_secret)
    except KeyError:
        if not (len(sys.argv) == 3):
            log.error("Arguments: client_id and client_secret")
            return 1
        server = OAuth2Server(*sys.argv[1:])

    server.browser_authorize()

    profile = server.fitbit.user_profile_get()
    log.info('You are authorized to access data for the user: {}'.format(
        profile['user']['fullName']))

    log.info('TOKEN\n=====\n')
    data = dict(server.fitbit.client.session.token.items())
    for key, value in server.fitbit.client.session.token.items():
        log.info('{} = {}'.format(key, value))
    with open(AUTH_FILE, 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, sort_keys=True) + os.linesep)

    return 0


if __name__ == '__main__':
    sys.exit(run())
