from setuptools import setup
import subprocess
import sys
from setuptools.command.test import test as TestCommand


class Test(TestCommand):

    def run_tests(self):
        raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', 'tests', '-v', '-s']))


setup(
    name='smallbusiness-framework',
    version='0.0.1a0',
    requires=[
        'yoyo',
        'pymysql',
        'psycopg2-binary',
        'sqlbuilder',
        'cached_property',
        'openpyxl',
        'weasyprint',
        'attrs',
        'num2words',
    ],
    extras_require={
        'dev': ['pytest']
    },
    package_data={
        'smallbusiness.framework': [
            'resource/*',
            'resource/template/*',
            'resource/template/css/*',
            'resource/template/html/*',
        ]
    },
    cmdclass={
        'test': Test
    },
    packages=[
        'smallbusiness.framework'
    ]
)
