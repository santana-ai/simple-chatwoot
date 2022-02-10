# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="simple_chatwoot",
    version="0.0.1",
    author="Henrique Santana",
    author_email="santana@cloudhumans.com",
    description="A super simple package to connect to Chatwoot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://simple-chatwoot.readthedocs.io/",
    project_urls={
        "Bug Tracker": "https://github.com/santana-ai/simple-chatwoot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["simple_chatwoot"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'requests>=2.27.1',
    ],
)