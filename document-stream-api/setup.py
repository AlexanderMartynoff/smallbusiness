from setuptools import setup
import subprocess
import sys
from setuptools.command.test import test as TestCommand


class Test(TestCommand):

    def run_tests(self):
        raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', 'tests', '-v', '-s']))


setup(
    name='document_stream_api',
    requirements=[
        'pymysql',
        'sqlbuilder',
        'cached_property',
        'openpyxl',
        'weasyprint',
    ],
    extras_require={
        'dev': ['pytest']
    },
    cmdclass={
        'test': Test
    }
)
