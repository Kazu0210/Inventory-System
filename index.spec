# -*- mode: python ; coding: utf-8 -*-

import os

# Set the distpath to place the executable outside the /app folder
distpath = os.path.abspath('../dist')  # Final .exe will be placed in /dist outside /app

# Analysis: gather information about the Python script and other resources
a = Analysis(
    ['app/index.py'],  # Main script is inside /app
    pathex=[],
    binaries=[],
    datas=[
        ('app/resources/*', 'resources'),  # Include resources folder (ensure it’s within allowed scope)
        ('app/src/*', 'src'),              # Include src folder (ensure it’s within allowed scope)
    ],
    hiddenimports=[
        'PyQt6.QtCharts', 
        'magic', 
        'plyer',
        'pymongo'
        ],  # Hidden imports for dependencies
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Create a Python bytecode archive
pyz = PYZ(a.pure)

# EXE: Bundle the application into an executable, setting custom distpath
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Inventory-System',  # Name of the output executable
    icon='app/resources/icons/system-icon.ico',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,  # Bundle everything into a single executable
    distpath=distpath  # Specify the custom distpath here (outside /app)
)
