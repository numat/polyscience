#!/usr/bin/env python
"""
Web interface for [VWR circulating baths]
(https://us.vwr.com/store/catalog/product.jsp?catalog_number=89203-002).

Distributed under the GNU General Public License v2
Copyright (C) 2015 NuMat Technologies
"""

import json
import os
import traceback
from tornado.ioloop import PeriodicCallback
import tornado.web
import tornado.websocket


def run_server(bath, port=10000):
    """Starts a web server on the specified port.

    Args:
        bath: An instance of `CirculatingBath` that is connected to the bath
            of interest.
        port: The port to serve the website. Default 10000.
    """
    class IndexHandler(tornado.web.RequestHandler):

        def get(self):
            self.render("index.template", port=port)

    class WebSocket(tornado.websocket.WebSocketHandler):

        def open(self):
            self.p = PeriodicCallback(self._loop, 500)
            self.p.start()

        def _loop(self):
            state = {"setpoint": bath.get_setpoint(),
                     "actual": bath.get_internal_temperature(),
                     "units": bath.get_temperature_units()}
            res = json.dumps({"result": state, "error": 0, "data": True},
                             separators=(",", ":"))
            self.write_message(res)

        def on_message(self, message):
            """Evaluates the function pointed to by json-rpc."""
            json_rpc = json.loads(message)

            try:
                result = getattr(bath,
                                 json_rpc["method"])(**json_rpc["params"])
                error = None
            except:
                result = traceback.format_exc()
                error = 1

            self.write_message(json.dumps({"result": result,
                                           "error": error,
                                           "id": json_rpc["id"]},
                                          separators=(",", ":")))

    handlers = [(r"/", IndexHandler), (r"/websocket", WebSocket),
                (r'/static/(.*)', tornado.web.StaticFileHandler,
                 {'path': os.path.normpath(os.path.dirname(__file__))})]
    application = tornado.web.Application(handlers)
    application.listen(port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        pass
