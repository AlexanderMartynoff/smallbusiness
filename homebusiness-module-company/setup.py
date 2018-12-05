from setuptools import setup


setup(
    name='homebusiness-module-company',
    install_requires=[
        'homebusiness-framework',
    ],
    package_data={
        'homebusiness.module.company': [
            'static/build/*',
            'static/build/css/font-awesome/css/*',
            'static/build/css/font-awesome/webfonts/*',
        ]
    },
    extras_require={
        'dev': ['pytest']
    },
    packages=[
        'homebusiness.module.company'
    ],
    include_package_data=True,
)
