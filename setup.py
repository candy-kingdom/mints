from setuptools import setup, find_packages

setup(
    name='mints',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Clean and elegant CLI development kit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[''],
    url='https://github.com/candy-kingdom/mints',
    author='Candy Kingdom',
    author_email='candy.kingdom.github@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
