# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../ContactAppUI/contacts_app.py'],
    pathex=['..'],  # Указываем корневой путь проекта
    binaries=[],
    datas=[],
    hiddenimports=['encodings'],
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
    name='contacts_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Отключает консольное окно
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='contacts_app.app',
    icon=None,  # Если есть иконка, укажите здесь путь к ней
    bundle_identifier='com.example.contactsapp',  # Уникальный идентификатор пакета
)