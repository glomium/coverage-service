#!/usr/bin/env python

import argparse
import logging
import os

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from tempfile import NamedTemporaryFile

import coverage


logger = logging.getLogger(__name__)


class Server(HTTPServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = coverage.CoverageData()
        self.report.write()


class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", str(os.path.getsize(self.server.report.base_filename())))
        self.end_headers()

    def do_GET(self):
        self.do_HEAD()
        with open(self.server.report.base_filename(), 'rb') as f:
            self.wfile.write(f.read())

    def do_DELETE(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.server.report.erase()

    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        with NamedTemporaryFile() as fp:
            fp.write(data)
            fp.flush()
            report = coverage.CoverageData(basename=fp.name)
            self.server.report.update(report)

        self.send_response(HTTPStatus.OK)
        self.end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify port [default: 8000]')
    args = parser.parse_args()

    with Server(('', args.port), Handler) as httpd:
        httpd.serve_forever()
