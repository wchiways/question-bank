# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for OCS题库系统
"""
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 获取当前目录
block_cipher = None
app_dir = os.path.join(os.getcwd(), 'app')

# 收集数据文件
datas = [
    (app_dir, 'app'),
    ('config.json', '.'),
    ('config.example.json', '.'),
]

# 收集隐式导入的模块
hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'sqlmodel',
    'sqlalchemy',
    'aiosqlite',
    'httpx',
    'pydantic',
    'pydantic_settings',
    'loguru',
    'app.core.config',
    'app.core.db',
    'app.core.logger',
    'app.api.v1.endpoints.query',
    'app.api.v1.router',
    'app.services.query_service',
    'app.services.ai_service',
    'app.services.cache_service',
    'app.utils.helpers',
]

# 收集所有数据文件
datas += collect_data_files('loguru')
datas += collect_data_files('httpx')

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas'],
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
    name='ocs-tiku',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
