import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import subprocess
import signal

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_modified = 0
        self.debounce_seconds = 1  # 防抖时间

    def on_modified(self, event):
        if event.is_directory:
            return
            
        # 检查是否在 __pycache__ 文件夹中
        if '__pycache__' in event.src_path:
            return
            
        current_time = time.time()
        if current_time - self.last_modified < self.debounce_seconds:
            return
            
        if event.src_path.endswith(('.py', '.html', '.js', '.css')):
            print(f"检测到文件变化: {event.src_path}")
            self.last_modified = current_time
            self.restart_callback()

class FileWatcher:
    def __init__(self, paths_to_watch, restart_callback):
        self.paths_to_watch = paths_to_watch
        self.observer = Observer()
        self.handler = FileChangeHandler(restart_callback)
        
    def start(self):
        for path in self.paths_to_watch:
            self.observer.schedule(self.handler, path, recursive=True)
        self.observer.start()
        print("文件监听已启动...")
        
    def stop(self):
        self.observer.stop()
        self.observer.join()
        print("文件监听已停止...")

def restart_application():
    print("正在重启应用...")
    if sys.platform.startswith('win'):
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        os.execv(sys.executable, [sys.executable] + sys.argv) 