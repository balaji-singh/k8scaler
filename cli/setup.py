from setuptools import setup, find_packages

setup(
    name="k8scaler-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "k8scaler=autoscaler_cli:cli",
        ],
    },
)
