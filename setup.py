from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

exec(open('seedfinder/version.py').read())

setup(
    name = 'seedfinder',
    version = __version__,
    description = 'Simple Python wrapper for seedfinder.eu\'s API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Hudson Bailey',
    author_email = 'hudsondiggsbailey@gmail.com',
    url="https://github.com/hdb/seedfinder-python",
    packages = ['seedfinder'],
    install_requires = ['requests'],
    license='MIT',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
