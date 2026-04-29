# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/python/main.py'],
    pathex=['src/python'],
    binaries=[],
    datas=[
        ('config/mods_data.json', 'config'),
    ],
    hiddenimports=[
        'mod_classifier',
        'logger',
        'config_manager',
        'jar_parser',
        'file_utils',
        'i18n',
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
    [],
    exclude_binaries=True,
    name='Minecraft-mod-classifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Minecraft-mod-classifier',
)
