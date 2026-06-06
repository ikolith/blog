import subprocess
import os
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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
            subprocess.run(["python", "scripts/makesite.py"], check=True, cwd=PROJECT_ROOT)
            print("Site rebuilt!")
        except subprocess.CalledProcessError:
            print("Build failed!")

def main():
    """Build site, start server, and watch for changes"""
    # Initial build
    subprocess.run(["python", "scripts/makesite.py"], check=True, cwd=PROJECT_ROOT)
    print("Initial build complete!")
    
    # Start file watcher
    event_handler = RebuildHandler()
    observer = Observer()
    observer.schedule(event_handler, "content", recursive=True)
    observer.schedule(event_handler, "layout", recursive=True)
    observer.schedule(event_handler, "static", recursive=True)
    observer.start()
    print("Watching for file changes...")
    
    # Start web server in background thread
    def start_server():
        os.chdir("_site")
        subprocess.run(["python", "-m", "http.server", "8000"])
    
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Server started at http://localhost:8000")
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