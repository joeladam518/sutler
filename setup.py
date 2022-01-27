from setuptools import setup, find_packages

setup(
    name='sutler',
    version='0.1',
    description="Command line utility to provision a multitude of computers.",
    url="https://github.com/joeladam518/sutler",
    author='Joel Haker',
    license='ISC',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'Click',
        'GitPython',
        'jinja2',
    ],
    extras_require={
        'build': [
            'pyinstaller'
        ],
    },
    entry_points={
        'console_scripts': [
            'sutler=sutler.main:cli',
        ],
    },
)
