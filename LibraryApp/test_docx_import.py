"""Quick diagnostic to verify python-docx is installed in the active venv."""
import sys

print('Python executable:', sys.executable)
try:
    import docx  # python-docx package
    ver = getattr(docx, '__version__', 'unknown')
    print('python-docx import: OK (version:', ver, ')')
except Exception as e:
    print('python-docx import: FAILED ->', e)
    print('Run to install:')
    print('  .\\.venv\\Scripts\\python.exe -m pip install python-docx')
