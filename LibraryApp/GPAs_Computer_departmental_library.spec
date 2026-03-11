# -*- mode: python ; coding: utf-8 -*-
# GPA's Computer Departmental Library - Complete Build Specification
# This spec file includes ALL features, dependencies, and files for a bug-free executable
# Build Date: 2026-03-11

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all
import os
import sys

block_cipher = None

# Get the current directory (LibraryApp folder)
current_dir = os.path.dirname(os.path.abspath(SPEC))

# Collect all matplotlib data files
matplotlib_datas = collect_data_files('matplotlib', include_py_files=True)
babel_datas = collect_data_files('babel')
tkcalendar_datas = collect_data_files('tkcalendar')

# DATA FILES - Include ALL necessary files
datas_list = [
    # Core database and configuration files
    ('library.db', '.'),
    ('requirements.txt', '.'),
    ('logo.png', '.'),
    ('logo.ico', '.'),
    ('library_settings.json', '.'),
    ('email_settings.json', '.'),
    ('app_config.json', '.'),
    ('sync_log.json', '.'),
    ('email_history.json', '.'),
    
    # Core Python modules (bundled as data files for reliability)
    ('database.py', '.'),
    ('database_pool.py', '.'),
    ('email_batch_service.py', '.'),
    ('sync_manager.py', '.'),
    ('config_manager.py', '.'),
    ('autocomplete_widget.py', '.'),
    ('login_loader.py', '.'),
    
    # Web Extension - Student Portal (COMPLETE)
    ('Web-Extension/student_portal.py', 'Web-Extension'),
    ('Web-Extension/run_waitress_portal.py', 'Web-Extension'),
    ('Web-Extension/portal.db', 'Web-Extension'),
    ('Web-Extension/.secret_key', 'Web-Extension'),
    
    # Web Extension Frontend - ALL files
    ('Web-Extension/frontend/dist', 'Web-Extension/frontend/dist'),
]

# Add collected data files from packages
datas_list.extend(matplotlib_datas)
datas_list.extend(babel_datas)
datas_list.extend(tkcalendar_datas)

# HIDDEN IMPORTS - Include ALL dependencies
hiddenimports_list = [
    # Core Python and tkinter
    'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 
    'tkinter.font', 'tkinter.scrolledtext', 'tkinter.colorchooser',
    '_tkinter', 'tkinter.constants', 'tkinter.dialog', 'tkinter.commondialog',
    
    # Data processing and Excel (COMPLETE)
    'pandas', 'pandas._libs', 'pandas._libs.tslibs', 'pandas.core', 
    'pandas.io', 'pandas.io.excel', 'pandas.io.formats', 
    'pandas.io.formats.excel', 'pandas.plotting', 'pandas.tseries',
    'openpyxl', 'openpyxl.cell', 'openpyxl.styles', 'openpyxl.workbook',
    'openpyxl.worksheet', 'openpyxl.utils', 'openpyxl.xml',
    'xlsxwriter', 'xlsxwriter.workbook', 'xlsxwriter.worksheet',
    'xlsxwriter.format', 'xlsxwriter.utility',
    'numpy', 'numpy.core', 'numpy.core._multiarray_umath',
    'numpy.random', 'numpy.linalg',
    
    # Document generation (Word and PDF)
    'docx', 'docx.shared', 'docx.enum', 'docx.enum.text', 'docx.oxml',
    'docx.text', 'docx.table', 'docx.document',
    'reportlab', 'reportlab.lib', 'reportlab.lib.pagesizes', 
    'reportlab.lib.colors', 'reportlab.lib.units', 'reportlab.lib.styles',
    'reportlab.lib.enums', 'reportlab.platypus', 'reportlab.pdfgen',
    'reportlab.pdfbase', 'reportlab.pdfbase.ttfonts',
    
    # Date and calendar
    'tkcalendar', 'tkcalendar.calendar_', 'tkcalendar.dateentry',
    'babel', 'babel.dates', 'babel.numbers', 'babel.localedata',
    'babel.core', 'babel.plural',
    
    # Plotting and visualization (COMPLETE matplotlib)
    'matplotlib', 'matplotlib.pyplot', 'matplotlib.figure',
    'matplotlib.backends', 'matplotlib.backends.backend_tkagg',
    'matplotlib.backends.backend_agg', 'matplotlib.backend_bases',
    'matplotlib.patches', 'matplotlib.dates', 'matplotlib.ticker',
    'matplotlib.axes', 'matplotlib.lines', 'matplotlib.path',
    'matplotlib.transforms', 'matplotlib.cbook', 'matplotlib.colors',
    'matplotlib.cm', 'matplotlib.colorbar', 'matplotlib.contour',
    'matplotlib.collections', 'matplotlib.font_manager',
    'matplotlib.mathtext', 'matplotlib.texmanager',
    
    # Web framework - Flask (COMPLETE)
    'flask', 'flask.app', 'flask.blueprints', 'flask.cli',
    'flask.config', 'flask.ctx', 'flask.globals', 'flask.helpers',
    'flask.json', 'flask.logging', 'flask.sessions', 'flask.signals',
    'flask.templating', 'flask.testing', 'flask.views', 'flask.wrappers',
    'werkzeug', 'werkzeug.routing', 'werkzeug.serving', 
    'werkzeug.security', 'werkzeug.utils', 'werkzeug.urls',
    'werkzeug.http', 'werkzeug.exceptions', 'werkzeug.datastructures',
    'werkzeug.wrappers', 'werkzeug.formparser', 'werkzeug.middleware',
    'jinja2', 'jinja2.ext', 'jinja2.loaders', 'jinja2.runtime',
    'jinja2.environment', 'jinja2.filters', 'jinja2.utils',
    'click', 'click.core', 'click.decorators', 'click.exceptions',
    'itsdangerous', 'itsdangerous.serializer', 'itsdangerous.signer',
    'markupsafe', 'markupsafe._native',
    
    # Web server - Waitress (COMPLETE)
    'waitress', 'waitress.server', 'waitress.task', 'waitress.channel',
    'waitress.adjustments', 'waitress.buffers', 'waitress.compat',
    'waitress.parser', 'waitress.receiver', 'waitress.rfc7230',
    'waitress.server', 'waitress.trigger', 'waitress.utilities',
    'waitress.wasyncore',
    
    # Database (SQLite and PostgreSQL)
    'sqlite3', '_sqlite3',
    'psycopg2', 'psycopg2.extensions', 'psycopg2.extras', 
    'psycopg2._psycopg', 'psycopg2.pool', 'psycopg2.errorcodes',
    'sqlalchemy', 'sqlalchemy.dialects', 'sqlalchemy.dialects.postgresql',
    'sqlalchemy.engine', 'sqlalchemy.pool', 'sqlalchemy.sql',
    
    # Image processing (COMPLETE)
    'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageDraw', 
    'PIL.ImageFont', 'PIL.ImageOps', 'PIL.ImageFilter',
    'PIL.ImageEnhance', 'PIL.ImageColor', 'PIL.ImageFile',
    'PIL.PngImagePlugin', 'PIL.JpegImagePlugin', 'PIL.BmpImagePlugin',
    'qrcode', 'qrcode.image', 'qrcode.image.pil', 'qrcode.image.svg',
    'qrcode.util',
    
    # Network, requests and email (COMPLETE)
    'socket', '_socket',
    'smtplib', 'ssl', '_ssl',
    'email', 'email.mime', 'email.mime.text', 'email.mime.base',
    'email.mime.multipart', 'email.mime.application', 'email.mime.image',
    'email.encoders', 'email.utils', 'email.header',
    'requests', 'requests.adapters', 'requests.auth', 'requests.cookies',
    'requests.exceptions', 'requests.hooks', 'requests.models',
    'requests.sessions', 'requests.structures', 'requests.utils',
    'urllib3', 'urllib3.connection', 'urllib3.connectionpool',
    'urllib3.exceptions', 'urllib3.poolmanager', 'urllib3.response',
    'urllib3.util', 'urllib3.util.retry', 'urllib3.contrib',
    'certifi',
    
    # Environment variables
    'dotenv', 'dotenv.main', 'dotenv.parser', 'dotenv.variables',
    
    # Core system utilities
    'webbrowser', 'subprocess', 'platform', 'threading', 'json',
    'io', 'os', 'sys', 'datetime', 'time', 'traceback',
    'collections', 'itertools', 'functools', 'operator',
    
    # Performance and optimization modules (custom)
    'database_pool', 'email_batch_service', 'sync_manager', 
    'config_manager', 'autocomplete_widget', 'login_loader',
    
    # Additional critical dependencies
    'pkg_resources', 'pkg_resources.py2_warn', 'pkg_resources._vendor',
    'six', 'six.moves', 'pytz', 'pytz.tzfile',
    'dateutil', 'dateutil.parser', 'dateutil.tz', 'dateutil.relativedelta',
    'charset_normalizer', 'idna', 'lxml', 'et_xmlfile',
    
    # Scientific computing support
    'scipy', 'scipy.sparse',
    
    # Encodings for text support
    'encodings', 'encodings.utf_8', 'encodings.cp1252', 'encodings.latin_1',
]

# Collect all submodules for critical packages
for package in ['pandas', 'numpy', 'matplotlib', 'flask', 'waitress', 'PIL']:
    try:
        hiddenimports_list.extend(collect_submodules(package))
    except:
        pass

# Remove duplicates
hiddenimports_list = list(set(hiddenimports_list))

# ANALYSIS
a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas_list,
    hiddenimports=hiddenimports_list,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude development and build artifacts
        'Web-Extension/frontend/node_modules',
        'Web-Extension/frontend/src',
        '__pycache__',
        '.git',
        'test',
        'tests',
        'testing',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ (Python zip archive)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE (Final executable)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GPAs_Computer_departmental_library',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window - pure GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',  # Windows icon file
    version=None,
)
