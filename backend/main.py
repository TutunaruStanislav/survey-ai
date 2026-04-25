import http.server
import socketserver
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from .services.survey_service import SurveyService
from .handlers import handle_get_questions, handle_post_answers


class SurveyHandler(http.server.SimpleHTTPRequestHandler):
    service = SurveyService()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/questions':
            handle_get_questions(self.service)(self)
        elif path == '/openapi.yaml':
            self.serve_openapi()
        elif path == '/docs':
            self.serve_swagger_ui()
        elif path == '/' or path.startswith('/'):
            self.serve_static(path)
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/answers':
            handle_post_answers(self.service)(self)
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serve_openapi(self):
        openapi_path = Path(__file__).parent.parent / 'openapi.yaml'
        if openapi_path.exists():
            with open(openapi_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/yaml')
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            self.send_error(404)

    def serve_swagger_ui(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({
            url: "/openapi.yaml",
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
            layout: "BaseLayout"
        })
    </script>
</body>
</html>'''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_static(self, path):
        if path == '/':
            path = '/index.html'

        frontend_dir = Path(__file__).parent.parent / 'frontend'
        file_path = frontend_dir / path.lstrip('/')

        if file_path.exists() and file_path.is_file():
            with open(file_path, 'rb') as f:
                content = f.read()

            content_type = self.get_content_type(str(file_path))
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)

    def get_content_type(self, file_path):
        if file_path.endswith('.html'):
            return 'text/html'
        elif file_path.endswith('.css'):
            return 'text/css'
        elif file_path.endswith('.js'):
            return 'application/javascript'
        elif file_path.endswith('.json'):
            return 'application/json'
        else:
            return 'application/octet-stream'

    def log_message(self, format, *args):
        print(f'{self.client_address[0]} - {format % args}')


class ThreadingHTTPServer(socketserver.ThreadingTCPServer):
    daemon_threads = True

    def server_bind(self):
        self.socket.setsockopt(socketserver.socket.SOL_SOCKET, socketserver.socket.SO_REUSEADDR, 1)
        super().server_bind()


def run_server(host='127.0.0.1', port=9000):
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, SurveyHandler)
    print(f'Server running at http://{host}:{port}')
    print(f'Swagger UI: http://{host}:{port}/docs')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
