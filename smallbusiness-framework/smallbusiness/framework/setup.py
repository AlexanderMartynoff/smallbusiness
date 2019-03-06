import sys
import subprocess

from .resource import FRAMEWORK_RESOURCE_DIR


def _apply_migrations():
    # see: https://stackoverflow.com/questions/163542/python-how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument
    # res = subprocess.call([sys.executable, '-m', 'yoyo', 'apply', './migrations'])

    with subprocess.Popen([
        sys.executable, '-m', 'yoyo', 'apply', '--config', 'yoyo.ini'
    ], cwd=FRAMEWORK_RESOURCE_DIR) as process:

        print(process)


def setup(api):
    _apply_migrations()
