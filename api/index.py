import os
import json
from http.server import BaseHTTPRequestHandler
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            update = json.loads(post_data.decode('utf-8'))

            if "chat_join_request" in update:
                join_request = update["chat_join_request"]
                chat_id = join_request["chat"]["id"]
                user_id = join_request["from"]["id"]

                url = f"https://api.telegram.org/bot{BOT_TOKEN}/approveChatJoinRequest"
                payload = {
                    "chat_id": chat_id,
                    "user_id": user_id
                }

                requests.post(url, json=payload)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Telegram Auto-Approve Bot Active!".encode('utf-8'))
      
