import json


def handle_post_answers(service):
    def handler(request_handler):
        content_length = int(request_handler.headers.get('Content-Length', 0))
        body = request_handler.rfile.read(content_length)

        try:
            answers_data = json.loads(body.decode('utf-8', errors='replace'))
        except (json.JSONDecodeError, ValueError) as e:
            request_handler.send_response(400)
            request_handler.send_header('Content-Type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.end_headers()
            request_handler.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode('utf-8'))
            return
        except Exception as e:
            request_handler.send_response(500)
            request_handler.send_header('Content-Type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.end_headers()
            request_handler.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        result = service.save_answers(answers_data)

        request_handler.send_response(200)
        request_handler.send_header('Content-Type', 'application/json')
        request_handler.send_header('Access-Control-Allow-Origin', '*')
        request_handler.end_headers()
        request_handler.wfile.write(json.dumps({
            'success': True,
            'message': 'Спасибо!',
            'submission': result
        }, ensure_ascii=False).encode('utf-8'))
    return handler
