# -*- mode: python -*-

block_cipher = None

import babelfish

a = Analysis(['guessit/__main__.py'],
             pathex=[],
             binaries=[],
             datas=[
                 ('guessit/config/*', 'guessit/config'),
                 ('guessit/data/*', 'guessit/data'),
                 (babelfish.__path__[0] + '/data', 'babelfish/data')
             ],
             hiddenimports=[
                 'pkg_resources.py2_warn',  # https://github.com/pypa/setuptools/issues/1963
                 'babelfish.converters.alpha2',
                 'babelfish.converters.alpha3b',
                 'babelfish.converters.alpha3t',
                 'babelfish.converters.name',
                 'babelfish.converters.opensubtitles',
                 'babelfish.converters.countryname'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='guessit',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True )