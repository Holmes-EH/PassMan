# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['PassMan.py'],
             pathex=['C:\\Users\\Samuel Holmes\\Documents\\Developer\\PassMan\\dist\\windowsBuild'],
             binaries=[],
             datas=[],
             hiddenimports=['passlib', 'configparser', 'passlib.handlers', 'passlib.handlers.pbkdf2', 'passlib.handlers.sha2_crypt', 'passlib.handlers.md5_crypt', 'passlib.handlers.des_crypt'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PassMan',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='..\\dist\\PassMan_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PassMan')
import shutil
shutil.copyfile('config.ini', '{0}/config.ini'.format(DISTPATH))