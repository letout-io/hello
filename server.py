from http.server import BaseHTTPRequestHandler, HTTPServer
from tabulate import tabulate
import os, platform, socket, uuid

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))
ip = s.getsockname()[0]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        messages = ['{}:{}'.format('Request ID', uuid.uuid4())]

        messages.append('{}: {}'.format('Node', platform.node()))
        messages.append('{}: {}'.format('Version', platform.version()))
        messages.append('{}: {}'.format('Architecture', platform.architecture()[0]))
        messages.append('{}: {}'.format('System', platform.system()))
        messages.append('{}: {}'.format('Release', platform.release()))
        messages.append('{}: {}'.format('IP Address', ip))

        messages.append('{}: {}'.format('Method', self.command))
        messages.append('{}: {}'.format('Path', self.path))


        messages.append('\nHeaders')
        table = []
        for item in self.headers.items():
            value = (item[1][:150] + '..') if len(item[1]) > 150 else item[1]
            table.append([item[0].ljust(50, '.'), value])
        messages.append(tabulate(table))

        messages.append('\nEnvironment Variables')
        table = []
        for key in os.environ:
            value = (os.environ[key][:150] + '...') if len(os.environ[key]) > 150 else os.environ[key]
            table.append([key.ljust(50, '.'), value])
        messages.append(tabulate(table))

        self.wfile.write(bytes("\n".join(messages), "utf8"))


with HTTPServer(('', 80), handler) as server:
    server.serve_forever()
