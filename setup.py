from setuptools import setup, find_packages

setup(
    name='sutler',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'jinja2'
        'packaging'
    ],
    entry_points='''
        [console_scripts]
        sutler=sutler.main:cli
    ''',
)
