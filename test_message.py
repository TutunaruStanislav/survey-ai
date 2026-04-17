#!/usr/bin/env python
import sys
sys.path.insert(0, 'backend')

from handlers.answers_handler import handle_post_answers
from services.survey_service import SurveyService

# Create a mock request handler
class MockRequestHandler:
    def __init__(self):
        self.headers = {'Content-Length': '0'}
        self.rfile = None
        self.wfile = MockWriter()
        self.response_code = None
        self.response_headers = {}

    def send_response(self, code):
        self.response_code = code

    def send_header(self, key, value):
        self.response_headers[key] = value

    def end_headers(self):
        pass

class MockWriter:
    def __init__(self):
        self.data = b''

    def write(self, data):
        self.data += data

# Test
service = SurveyService()
handler = handle_post_answers(service)

# Create a proper request
import json
mock = MockRequestHandler()
answers = {'q1': 'Test', 'q2': '30', 'q3': '5', 'q4': 'Good', 'q5': 'Yes'}
mock.headers = {'Content-Length': len(json.dumps(answers))}

# Create a mock rfile
class MockRFile:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read(self, size):
        result = self.data[self.pos:self.pos+size]
        self.pos += size
        return result

mock.rfile = MockRFile(json.dumps(answers).encode('utf-8'))

# Call the handler
handler(mock)

# Check the response
response_data = json.loads(mock.wfile.data.decode('utf-8'))
print(f"Message: '{response_data['message']}'")
print(f"Expected: 'Спасибо!'")
print(f"Match: {response_data['message'] == 'Спасибо!'}")
