# -*- mode: python ; coding: utf-8 -*-

hiddenimports=[
    'pandas','openpyxl','xlsxwriter','sqlite3','tkinter','tkinter.ttk','tkinter.messagebox','tkinter.filedialog','datetime','webbrowser','subprocess','platform'
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('library.db','.')],
    hiddenimports=hiddenimports,
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
    name='LibraryOfComputerDepartment_v3.4.3_FINAL_CLEAN',
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
    version=None,
    uac_admin=False,
    uac_uiaccess=False,
)
