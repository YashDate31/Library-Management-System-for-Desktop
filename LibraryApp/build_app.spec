# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('library.db', '.'),
        ('requirements.txt', '.'),
        ('logo.png', '.'),
        ('Web-Extension/student_portal.py', 'Web-Extension'),
        ('Web-Extension/portal.db', 'Web-Extension'),
        ('Web-Extension/frontend/dist', 'Web-Extension/frontend/dist'),
    ],
    hiddenimports=[
        'pandas', 'openpyxl', 'docx', 'tkcalendar',
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog',
        'matplotlib', 'matplotlib.pyplot', 'matplotlib.backends.backend_tkagg',
        'matplotlib.figure', 'matplotlib.patches', 'numpy', 'xlsxwriter',
        'flask', 'werkzeug', 'jinja2', 'click', 'itsdangerous', 'markupsafe'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['Web-Extension/frontend/node_modules', 'Web-Extension/frontend/src'],
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
    name='LibraryManagementSystem_v5.0_FINAL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)