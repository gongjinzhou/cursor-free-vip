import sys
import queue
from threading import Lock

class WebPrintRedirect:
    def __init__(self):
        self.output_queue = queue.Queue()
        self.translation_key_queue = queue.Queue()  # 新增翻译key队列
        self.lock = Lock()
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self.current_translation_key = None  # 当前翻译key
        
    def write(self, text):
        # 确保原始输出仍然可用
        self._original_stdout.write(text)
        # 将输出和当前翻译key放入队列
        with self.lock:
            self.output_queue.put(text)
            self.translation_key_queue.put(self.current_translation_key)
            
    def flush(self):
        self._original_stdout.flush()
        
    def set_translation_key(self, key):
        """设置当前翻译key"""
        self.current_translation_key = key
        
    def get_output(self):
        """获取所有累积的输出及其对应的翻译key"""
        output = []
        keys = []
        with self.lock:
            while not self.output_queue.empty():
                text = self.output_queue.get()
                key = self.translation_key_queue.get()
                output.append(text)
                keys.append(key)
        return {
            'text': ''.join(output),
            'keys': keys
        }
    
    def enable(self):
        """启用重定向"""
        sys.stdout = self
        sys.stderr = self
        
    def disable(self):
        """禁用重定向"""
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

# 创建全局实例
web_print = WebPrintRedirect() 