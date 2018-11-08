import os
from setuptools import setup, find_packages

__version__ = '0.2.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'navmplot',
    version = __version__,
    author = 'Yuanyuan Cen',
    author_email = 'yycen@live.com',
    url = 'https://github.com/yycen/navmplot',
    description = 'Provide a interface to plotting data with Naver Maps with Python',
    long_description=read('README.rst'),
    license='MIT',
    keywords='python wrapper naver maps',
    packages = find_packages(),
    include_package_data=True,
    package_data = {
        'navmplot': ['markers/*.png'],
    },
    install_requires=['requests'],
)
