from setuptools import setup, find_packages

setup(
    name='candy-cli',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Tools for writing clean CLI code.',
    long_description=open('README.md').read(),
    install_required=[''],
    url='https://github.com/candy-kingdom/cli',
    author='Candy Kingdom',
    author_email='candy.kingdom.github@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
