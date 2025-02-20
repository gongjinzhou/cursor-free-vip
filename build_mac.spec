# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('turnstilePatch', 'turnstilePatch'),
        ('PBlock', 'PBlock'),
        ('locales', 'locales'),
        ('cursor_auth.py', '.'),
        ('reset_machine_manual.py', '.'),
        ('cursor_register.py', '.'),
        ('browser.py', '.'),
        ('control.py', '.'),
        ('.env', '.')
    ],
    hiddenimports=[
        'cursor_auth',
        'reset_machine_manual',
        'browser',
        'control'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CursorFreeVIP_1.0.0_mac_universal2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=true,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
    icon='images/logo.ico' if os.path.exists('images/logo.ico') else None
)
