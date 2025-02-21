import webview
import os
import sys
import json
from colorama import Fore, Style, init
import reset_machine_manual
import cursor_register
import cursor_register_manual
import quit_cursor
from print_redirect import web_print
from file_watcher import FileWatcher
import threading
import ctypes

# 隐藏控制台窗口并不在任务栏中显示
if hasattr(sys, '_MEIPASS'):
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # 隐藏窗口
        ctypes.windll.user32.SetWindowLong(hwnd, -16, 0x80000000)  # 不在任务栏中显示
    except:
        pass

class Api:
    def __init__(self, translator):
        self.translator = translator
        # 启用print重定向
        web_print.enable()

    def get_translations(self):
        """获取当前语言的所有翻译"""
        return self.translator.translations.get(self.translator.current_language, {})

    def set_language(self, lang_code):
        """设置语言"""
        return self.translator.set_language(lang_code)

    def get_available_languages(self):
        """获取可用的语言列表"""
        return self.translator.get('languages')

    def reset_machine(self):
        """重置机器"""
        return reset_machine_manual.run(self.translator)

    def register(self):
        """注册"""
        try:
            result = cursor_register.main(self.translator)
            return {"success": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def register_manual(self):
        """手动注册"""
        try:
            result = cursor_register_manual.main(self.translator)
            return {"success": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_print_output(self):
        """获取累积的print输出"""
        return web_print.get_output()

    def quit_cursor(self):
        """退出Cursor"""
        web_print.disable()  # 退出前禁用重定向
        return quit_cursor.quit_cursor(self.translator)

class Translator:
    def __init__(self):
        self.current_language = 'zh_tw'  # 默认语言
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """加载所有可用的翻译"""
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        if hasattr(sys, '_MEIPASS'):
            locales_dir = os.path.join(sys._MEIPASS, 'locales')
            
        for file in os.listdir(locales_dir):
            if file.endswith('.json'):
                lang_code = file[:-5]  # 移除 .json
                with open(os.path.join(locales_dir, file), 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
    
    def get(self, key, **kwargs):
        """获取翻译文本"""
        try:
            keys = key.split('.')
            value = self.translations.get(self.current_language, {})
            web_print.set_translation_key(key)  # 设置当前翻译key
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, key)
                else:
                    return key
            return value.format(**kwargs) if kwargs else value
        except Exception:
            return key
    
    def set_language(self, lang_code):
        """设置当前语言"""
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False

def main():
    translator = Translator()
    api = Api(translator)

    # 获取HTML文件路径
    html_path = os.path.join(os.path.dirname(__file__), 'web', 'index.html')
    if hasattr(sys, '_MEIPASS'):
        html_path = os.path.join(sys._MEIPASS, 'web', 'index.html')

    # 设置要监听的目录
    paths_to_watch = [
        os.path.dirname(__file__),  # 监听Python文件
        os.path.join(os.path.dirname(__file__), 'web')  # 监听前端文件
    ]
    
    # 创建文件监听器
    watcher = FileWatcher(paths_to_watch, lambda: os.execv(sys.executable, [sys.executable] + sys.argv))
    
    # 在新线程中启动文件监听
    watcher_thread = threading.Thread(target=watcher.start, daemon=True)
    watcher_thread.start()

    # 创建窗口
    window = webview.create_window(
        'Cursor VIP Tools',
        html_path,
        js_api=api,
        width=800,
        height=600,
        resizable=True,
        frameless=False,
        easy_drag=True,
        text_select=False,
        on_top=False,
        confirm_close=True,
        background_color='#FFFFFF'
    )
    
    try:
        webview.start(debug=False)
    finally:
        watcher.stop()  # 确保在程序退出时停止文件监听

if __name__ == '__main__':
    main() 