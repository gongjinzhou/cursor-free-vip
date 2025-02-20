import warnings
import os
import platform
import subprocess
import time
import threading
import shutil
from subprocess import run

# 忽略特定警告
warnings.filterwarnings("ignore", category=SyntaxWarning)

class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.animation_thread = None

    def start(self, message="Building"):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate, args=(message,))
        self.animation_thread.start()

    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        print("\r" + " " * 70 + "\r", end="", flush=True)

    def _animate(self, message):
        animation = "|/-\\"
        idx = 0
        while self.is_running:
            print(f"\r{message} {animation[idx % len(animation)]}", end="", flush=True)
            idx += 1
            time.sleep(0.1)

def progress_bar(progress, total, prefix="", length=50):
    filled = int(length * progress // total)
    bar = "█" * filled + "░" * (length - filled)
    percent = f"{100 * progress / total:.1f}"
    print(f"\r{prefix} |{bar}| {percent}% Complete", end="", flush=True)
    if progress == total:
        print()

def simulate_progress(message, duration=1.0, steps=20):
    print(f"\033[94m{message}\033[0m")
    for i in range(steps + 1):
        time.sleep(duration / steps)
        progress_bar(i, steps, prefix="Progress:", length=40)

def clean_build():
    """清理build和dist目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理 {dir_name} 目录")

def create_spec_file(is_mac=False):
    """创建spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 定义需要包含的数据文件
datas = [
    ('web', 'web'),
    ('locales', 'locales'),
]

a = Analysis(
    ['web_main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'webview',
        'watchdog',
        'colorama',
        'requests',
        'psutil',
        'DrissionPage',
        'threading',
        'json',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CursorVIP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)'''

    spec_file = 'build_mac.spec' if is_mac else 'build_windows.spec'
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print(f"已创建 {spec_file}")

def build():
    """执行打包"""
    clean_build()
    
    # 检测操作系统
    is_mac = platform.system() == 'Darwin'
    spec_file = 'build_mac.spec' if is_mac else 'build_windows.spec'
    
    # 创建spec文件
    create_spec_file(is_mac)
    
    # 执行打包命令
    cmd = ['pyinstaller', '--clean', spec_file]
    result = run(cmd)
    
    if result.returncode == 0:
        print("打包成功！")
        print(f"可执行文件位于 dist/CursorVIP{'app' if is_mac else '.exe'}")
    else:
        print("打包失败！")

if __name__ == '__main__':
    build() 