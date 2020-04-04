#!/usr/bin/env python

import argparse
import os
import socketserver

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

import coverage


class Handler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = None

    def do_HEAD(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/octet-stream")
        self.end_headers()

    def do_GET(self):
        if self.report is None:
            self.report = coverage.CoverageData(no_disk=True)
        data = self.report.dumps()

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)

    def do_DELETE(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()

        self.report = None

    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        report = coverage.CoverageData(no_disk=True)

        if self.report is None:
            self.report = report
        else:
            self.report.update(report)

        self.send_response(HTTPStatus.OK)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify port [default: 8000]')
    args = parser.parse_args()

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        httpd.serve_forever()
