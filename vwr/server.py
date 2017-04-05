#!/usr/bin/env python
"""
Web interface for [VWR circulating baths]
(https://us.vwr.com/store/catalog/product.jsp?catalog_number=89203-002).

Distributed under the GNU General Public License v2
Copyright (C) 2015 NuMat Technologies
"""
import getpass
import hashlib
import json
import os
import time
import traceback

from tornado.ioloop import PeriodicCallback
import tornado.web
import tornado.websocket

root = os.path.normpath(os.path.dirname(__file__))
password_path = os.path.join(root, 'password.txt')


def set_password():
    """Called by `--set-password`, this sets a new password."""
    digest = hashlib.sha512(getpass.getpass().encode('utf-8')).hexdigest()
    with open(password_path, 'w') as out_file:
        out_file.write(digest)
    return digest


def get_password():
    """Gets password if already set, forwards to `set_password` otherwise."""
    if os.path.exists(password_path):
        with open(password_path) as in_file:
            password = in_file.read().strip()
    else:
        password = set_password()
    return password


def run_server(bath, port=50000, require_login=False):
    """Starts a web server on the specified port.

    Args:
        bath: An instance of `CirculatingBath` that is connected to the bath
            of interest.
        port: The port to serve the website. Default 50000.
        require_login: If True, serves a login page
    """
    if require_login:
        password = get_password()

    class IndexHandler(tornado.web.RequestHandler):

        def get(self):
            if require_login and not self.get_secure_cookie('vwr'):
                self.redirect('/login')
            else:
                self.render('index.template', port=port)

    class LoginHandler(tornado.web.RequestHandler):

        def get(self):
            self.render('login.template')

        def post(self):
            submitted_pass = self.get_argument('password', '').encode('utf-8')
            if hashlib.sha512(submitted_pass).hexdigest() == password:
                self.set_secure_cookie('vwr', str(time.time()))
                self.redirect('/')
            else:
                time.sleep(1)
                self.redirect(u'/login?error')

    class WebSocket(tornado.websocket.WebSocketHandler):

        def open(self):
            self.p = PeriodicCallback(self._loop, 500)
            self.p.start()

        def _loop(self):
            state = {'setpoint': bath.get_setpoint(),
                     'actual': bath.get_internal_temperature(),
                     'units': bath.get_temperature_units()}
            res = json.dumps({'result': state, 'error': 0, 'data': True},
                             separators=(',', ':'))
            self.write_message(res)

        def on_message(self, message):
            """Evaluates the function pointed to by json-rpc."""
            json_rpc = json.loads(message)

            try:
                result = getattr(bath,
                                 json_rpc['method'])(**json_rpc['params'])
                error = None
            except:
                result = traceback.format_exc()
                error = 1

            self.write_message(json.dumps({'result': result,
                                           'error': error,
                                           'id': json_rpc['id']},
                                          separators=(',', ':')))

        def on_close(self):
            """Stops looping calls on close."""
            self.p.stop()

    handlers = [(r'/', IndexHandler), (r'/login', LoginHandler),
                (r'/websocket', WebSocket),
                (r'/static/(.*)', tornado.web.StaticFileHandler,
                 {'path': root})]
    if require_login:
        application = tornado.web.Application(handlers, cookie_secret=password)
    else:
        application = tornado.web.Application(handlers)
    application.listen(port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        pass
