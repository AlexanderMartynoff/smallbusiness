from setuptools import setup


setup(
    name='smallbusiness-module-company',
    version='0.0.1a0',
    install_requires=[
        'smallbusiness-framework',
    ],
    package_data={
        'smallbusiness.module.company': [
            'static/build/*',
            'static/build/css/font-awesome/css/*',
            'static/build/css/font-awesome/webfonts/*',
            'resource/*',
        ]
    },
    extras_require={
        'dev': ['pytest']
    },
    packages=[
        'smallbusiness.module.company'
    ],
    include_package_data=True,
)
