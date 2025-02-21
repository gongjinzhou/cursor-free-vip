# -*- mode: python ; coding: utf-8 -*-

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
    icon='images/logo.ico' if os.path.exists('images/logo.ico') else None,
    uac_admin=False
)