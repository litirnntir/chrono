# код для запуска: python setup.py py2app -A

from setuptools import setup

APP_NAME = 'Chrono'
APP = ['main.py']
DATA_FILES = ['background.png']
OPTIONS = {
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': 'Crono control',
    },
    'iconfile': 'chrono.icns',
    'packages': ['PyQt6']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
