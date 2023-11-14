import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'Restarting...')
        run_script()

def run_script():
    subprocess.run(['python', 'run.py'])

if __name__ == "__main__":
    run_script()
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
