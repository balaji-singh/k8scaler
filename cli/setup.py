from setuptools import setup, find_packages

setup(
    name='autoscaler_cli',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Click'
    ],
)
