from distutils.core import setup

from setuptools import find_packages

setup(
    name = 'gak',
    packages = find_packages(),
	scripts=['scripts/gak'],
    version = '0.1.1',
    description = 'Command-line tool to make local Git repo interaction more efficient',
    author = 'Samuel Longchamps',
    author_email = 'samuel.longchamps@usherbrooke.ca',
    url = 'https://github.com/SamuelLongchamps/gak',
    download_url = 'https://github.com/SamuelLongchamps/gak/releases',
    keywords = ['git', 'ak', 'cli', 'tool'],
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: MIT',
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha'
    ],
)
