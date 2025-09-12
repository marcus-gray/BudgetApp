"""
PyInstaller specification file for Budget App.
This script creates the build configuration for packaging the application.
"""

import sys
import os
from pathlib import Path

# Application details
APP_NAME = "BudgetApp"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Modern Python-based monthly budgeting application"
APP_AUTHOR = "Budget App Team"

def create_spec_content():
    """Generate PyInstaller spec file content."""
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path.cwd() / 'src'
sys.path.insert(0, str(src_path))

block_cipher = None

# Data files to include
datas = []

# Hidden imports for CustomTkinter and other dependencies
hiddenimports = [
    'customtkinter',
    'tkinter',
    'tkinter.ttk',
    'PIL',
    'PIL._tkinter_finder',
    'bcrypt',
    'sqlite3',
    'secrets',
    'uuid',
    'datetime',
    'decimal',
    'pathlib',
    'contextlib',
    're',
    'time',
    'typing',
]

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
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
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='assets/icon.ico' if sys.platform == 'win32' else 'assets/icon.icns',
)

# macOS App bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='{APP_NAME}.app',
        icon='assets/icon.icns',
        bundle_identifier='com.budgetapp.desktop',
        version='{APP_VERSION}',
        info_plist={{
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleName': '{APP_NAME}',
            'CFBundleDisplayName': '{APP_NAME}',
            'CFBundleVersion': '{APP_VERSION}',
            'CFBundleShortVersionString': '{APP_VERSION}',
            'NSHumanReadableCopyright': 'Copyright © 2024 {APP_AUTHOR}',
            'NSHighResolutionCapable': True,
        }},
    )
"""
    
    return spec_content

if __name__ == "__main__":
    spec_content = create_spec_content()
    
    with open("BudgetApp.spec", "w") as f:
        f.write(spec_content)
    
    print("✅ PyInstaller spec file created: BudgetApp.spec")
    print("Run: pyinstaller BudgetApp.spec")