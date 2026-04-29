# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# 使用正斜杠确保跨平台兼容
script_path = 'src/python/main.py'
config_data = ('config/mods_data.json', 'config')

a = Analysis(
    [script_path],
    pathex=['src/python'],
    binaries=[],
    datas=[config_data],
    hiddenimports=['mod_classifier', 'logger', 'config_manager', 'jar_parser', 'file_utils', 'i18n'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Minecraft-mod-classifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Minecraft-mod-classifier',
)
