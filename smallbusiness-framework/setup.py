from setuptools import setup
from os.path import dirname, join
import subprocess
import sys
from babel.messages.frontend import (
    update_catalog,
    compile_catalog,
    init_catalog,
    extract_messages
)
from setuptools.command.test import test
from smallbusiness.framework.resource import FRAMEWORK_DIR, FRAMEWORK_RESOURCE_DIR


class Test(test):
    def run_tests(self):
        raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', 'tests', '-v', '-s']))


class UpdateMessages(update_catalog):
    def finalize_options(self):
        if not self.locale:
            self.locale = 'ru'

        self.domain = 'framework'
        self.input_file = join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale/framework.pot')
        self.output_dir = join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale')

        super().finalize_options()


class CompileMessages(compile_catalog):
    def finalize_options(self):
        self.domain = 'framework'
        self.directory = join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale')

        super().finalize_options()


class InitMessages(init_catalog):
    def finalize_options(self):
        if not self.locale:
            self.locale = 'ru'

        self.domain = 'framework'

        self.input_file = join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale/framework.pot')
        self.output_dir = join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale')

        super().finalize_options()


class ExtractMessages(extract_messages):
    def finalize_options(self):
        self.output_file = join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale/framework.pot')
        self.mapping_file = join(FRAMEWORK_RESOURCE_DIR, 'i18n/babel-mapping.ini')
        self.input_dirs = [FRAMEWORK_DIR]

        super().finalize_options()


setup(
    name='smallbusiness-framework',
    version='0.0.1a0',
    install_requires=[
        'ruamel.yaml',
        'PyJWT',
        'falcon',
        'yoyo-migrations',
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
        'test': Test,
        'extractmsg': ExtractMessages,
        'initmsg': InitMessages,
        'compilemsg': CompileMessages,
        'updatemsg': UpdateMessages,
    },
    packages=[
        'smallbusiness.framework'
    ]
)
