import PyInstaller.__main__
import os

hidden_imports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'keyboard',
    'json',
    'os',
    'sys',
    'pathlib',
    'base64',
    'threading',
    'time'
]

args = [
    'main.py',
    '--onefile',
    '--noconsole',
    '--name=ClipMate',
    '--clean',
    '--distpath=./dist',
    '--workpath=./build',
    '--specpath=./',
    '--upx-dir=C:/upx' if os.name == 'nt' else '--upx-dir=/usr/local/bin',
]

for imp in hidden_imports:
    args.append(f'--hidden-import={imp}')

args.append('--add-data=src;src')

if os.path.exists('icon.ico'):
    args.append('--icon=icon.ico')

print(f"Выполняем команду: pyinstaller {' '.join(args)}")

PyInstaller.__main__.run(args)