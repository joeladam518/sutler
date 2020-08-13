from setuptools import setup, find_packages

setup(
    name='provision_me',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'jinja2'
    ],
    entry_points='''
        [console_scripts]
        provisioner=provisioner.main:cli
    ''',
)
