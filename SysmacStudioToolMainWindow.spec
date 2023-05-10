# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['SysmacStudioToolMainWindow.py'],  # 打包的.py文件
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\sqqian\\Desktop\\sysmac_studio_enhanced_tool\\data\\*.pdf', 'data'), 
    ('C:\\Users\\sqqian\\Desktop\\sysmac_studio_enhanced_tool\\images\\*.svg', 'images')],  # 将所有.xlsx文件导入到data文件夹下（在打包后的程序里会增加data文件夹保存.xlsl文件’），以2元组的格式指定(src,dest)，多个文件时用逗号将元祖隔开。
    hiddenimports=[],
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
    name='SysmacStudioEnhancedTool',  # 设置.exe可执行文件的名字
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 是否显示cmd窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
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
    upx=True,
    upx_exclude=[],
    name='SysmacStudioToolMainWindow',
)
