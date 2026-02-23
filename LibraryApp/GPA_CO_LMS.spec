# -*- mode: python ; coding: utf-8 -*-
# GPA_CO_LMS Build Specification
# Complete build configuration with ALL features and dependencies

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        # Core database and configuration files
        ('library.db', '.'),
        ('requirements.txt', '.'),
        ('logo.png', '.'),
        ('library_settings.json', '.'),
        ('email_settings.json', '.'),
        ('app_config.json', '.'),
        ('sync_log.json', '.'),
        ('email_history.json', '.'),
        
        # Core Python modules
        ('database.py', '.'),
        ('database_pool.py', '.'),
        ('email_batch_service.py', '.'),
        ('sync_manager.py', '.'),
        ('config_manager.py', '.'),
        ('autocomplete_widget.py', '.'),
        ('login_loader.py', '.'),
        
        # Web Extension - Student Portal
        ('Web-Extension/student_portal.py', 'Web-Extension'),
        ('Web-Extension/run_waitress_portal.py', 'Web-Extension'),
        ('Web-Extension/portal.db', 'Web-Extension'),
        ('Web-Extension/frontend/dist', 'Web-Extension/frontend/dist'),
    ],
    hiddenimports=[
        # Core Python modules
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.font',
        
        # Data processing and Excel
        'pandas', 'openpyxl', 'xlsxwriter', 'numpy',
        'pandas.core', 'pandas.io', 'pandas.io.excel', 'pandas.io.formats', 'pandas.io.formats.excel',
        
        # Document generation
        'docx', 'docx.shared', 'docx.enum', 'docx.enum.text',
        'reportlab', 'reportlab.lib', 'reportlab.lib.pagesizes', 'reportlab.lib.colors',
        'reportlab.lib.units', 'reportlab.platypus', 'reportlab.lib.styles', 'reportlab.lib.enums',
        
        # Date and calendar
        'tkcalendar', 'babel', 'babel.dates', 'babel.numbers',
        
        # Plotting and visualization
        'matplotlib', 'matplotlib.pyplot', 'matplotlib.backends', 'matplotlib.backends.backend_tkagg',
        'matplotlib.figure', 'matplotlib.patches', 'matplotlib.dates',
        
        # Web framework - Flask
        'flask', 'flask.json', 'flask.templating',
        'werkzeug', 'werkzeug.routing', 'werkzeug.serving', 'werkzeug.security',
        'jinja2', 'jinja2.ext',
        'click', 'itsdangerous', 'markupsafe',
        
        # Web server - Waitress
        'waitress', 'waitress.server',
        
        # Database
        'sqlite3',
        'psycopg2', 'psycopg2.extensions', 'psycopg2.extras', 'psycopg2._psycopg',
        'sqlalchemy', 'sqlalchemy.dialects', 'sqlalchemy.dialects.postgresql',
        
        # Image processing
        'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageDraw', 'PIL.ImageFont',
        'qrcode', 'qrcode.image', 'qrcode.image.pil',
        
        # Network and requests
        'socket', 'smtplib', 'email', 'email.mime', 'email.mime.text',
        'email.mime.multipart', 'email.mime.application',
        'requests', 'urllib3',
        
        # Environment variables
        'dotenv', 'python-dotenv',
        
        # System utilities
        'webbrowser', 'subprocess', 'platform', 'threading', 'json', 'io',
        
        # Performance and optimization modules
        'database_pool', 'email_batch_service', 'sync_manager', 'config_manager',
        
        # Additional dependencies
        'pkg_resources', 'pkg_resources.py2_warn',
        'six', 'pytz', 'dateutil', 'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude development and build artifacts
        'Web-Extension/frontend/node_modules',
        'Web-Extension/frontend/src',
    ],
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
    name='GPA_CO_LMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png',  # Application icon
)
