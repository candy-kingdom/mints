from io import open
from re import search
from os import linesep
from setuptools import setup, find_packages


PATH = 'candies/cli'


def version():
    with open(f'{PATH}/__init__.py', 'rt', encoding='utf8') as f:
        version = search(r"__version__ = \'(.*?)\'", f.read()).group(1)
    return version


def readme():
    with open('README.md', 'rt', encoding='utf8') as f:
        readme = f.read()
    return readme


def requirements(filename='requirements.txt'):
    with open(filename, 'rt', encoding='utf-8') as stream:
        content = stream.read()
    return [line for line in content.split(linesep)
            if not line.strip().startswith('#')]


setup(
    name='candy-cli',
    version=version(),
    description='Tools for writing clean CLI code.',
    long_description=readme(),
    author='Candy Kingdom',
    author_email='candy.kingdom.github@gmail.com',
    url='https://github.com/candy-kingdom/cli',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7.4',
    ],
)
