import subprocess
import os
import threading
import time
import http.server
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_base_path():
    params_file = os.path.join(PROJECT_ROOT, 'params.json')
    if os.path.isfile(params_file):
        return json.load(open(params_file)).get('base_path', '')
    return ''

class RebuildHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File changed: {event.src_path}")
            self.rebuild()

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.rebuild()

    def rebuild(self):
        try:
            subprocess.run(["python3", "scripts/makesite.py"], check=True, cwd=PROJECT_ROOT)
            print("Site rebuilt!")
        except subprocess.CalledProcessError:
            print("Build failed!")

def make_handler(base_path):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            if base_path and path.startswith(base_path):
                path = path[len(base_path):] or '/'
            return super().translate_path(path)

        def log_message(self, format, *args):
            print(format % args)

    return Handler

def main():
    subprocess.run(["python3", "scripts/makesite.py"], check=True, cwd=PROJECT_ROOT)
    print("Initial build complete!")

    event_handler = RebuildHandler()
    observer = Observer()
    observer.schedule(event_handler, "content", recursive=True)
    observer.schedule(event_handler, "layout", recursive=True)
    observer.schedule(event_handler, "static", recursive=True)
    observer.start()
    print("Watching for file changes...")

    base_path = get_base_path()
    site_dir = os.path.join(PROJECT_ROOT, '_site')

    def start_server():
        os.chdir(site_dir)
        handler = make_handler(base_path)
        httpd = http.server.HTTPServer(('', 8000), handler)
        httpd.serve_forever()

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    print(f"Server started at http://localhost:8000{base_path}/")
    print("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping...")

    observer.join()

if __name__ == "__main__":
    main()
