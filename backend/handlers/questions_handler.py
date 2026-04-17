import json


def handle_get_questions(service):
    def handler(request_handler):
        questions = service.get_questions()
        request_handler.send_response(200)
        request_handler.send_header('Content-Type', 'application/json')
        request_handler.send_header('Access-Control-Allow-Origin', '*')
        request_handler.end_headers()
        request_handler.wfile.write(json.dumps(questions).encode())
    return handler
