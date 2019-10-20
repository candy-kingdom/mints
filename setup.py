from re import search
from setuptools import setup, find_packages


PATH = 'candies/cli'


def text_of(path):
    with open(path, 'rt', encoding='utf8') as file:
        return file.read()


def version():
    text = text_of(f'{PATH}/__init__.py')
    match = search(r"__version__ = \'(.*?)\'", text)

    return match.group(1)


def readme():
    return text_of('README.md')


def requirements():
    return text_of('requirements.txt')


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
        'Programming Language :: Python :: 3.8.0',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
