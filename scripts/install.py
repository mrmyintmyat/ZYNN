import os
import shutil
import requests
import zipfile
import tarfile
import platform
import time
from termcolor import colored
from tqdm import tqdm

def install_cloudflared(httpd, port):
    cloudflared_path = "server/cloudflared"

    if os.path.exists(cloudflared_path):
        # print(colored(f"\n[+] Cloudflared already installed.", color='yellow'))
        time.sleep(0.03)
    else:
        # print(colored(f"\n[+] Installing Cloudflared...", color='yellow'))
        system_architecture = platform.machine()

        if "arm" in system_architecture or "Android" in system_architecture:
            download('https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm', 'cloudflared')
        elif "aarch64" in system_architecture:
            download('https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64', 'cloudflared')
        elif "x86_64" in system_architecture:
            download('https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64', 'cloudflared')
        else:
            download('https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386', 'cloudflared')
        from scripts.server import start_cloudflared
        start_cloudflared(httpd, port)

def download(url, output):
    file_name = os.path.basename(url)
    if os.path.exists(file_name) or os.path.exists(output):
        shutil.rmtree(file_name, ignore_errors=True)
        shutil.rmtree(output, ignore_errors=True)

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with tqdm.wrapattr(open(file_name, 'wb'), 'write', miniters=1,
                               total=int(response.headers.get('content-length', 0)),
                               desc=f"\033[93mDownloading {output}\033[0m ",  # Use ANSI escape code for yellow color
                               unit='B', unit_scale=True) as file:
                shutil.copyfileobj(response.raw, file)

        # Explicitly close the file
        file.close()

        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall(output)
        elif file_name.endswith('.tgz'):
            with tarfile.open(file_name, 'r:gz') as tar_ref:
                tar_ref.extractall(output)
        else:
            shutil.move(file_name, os.path.join('server', output))

        os.chmod(os.path.join('server', output), 0o755)

    except Exception as e:
        print(f"\nError occurred while downloading {output}: {e}")
        exit(1)
