from setuptools import find_packages, setup

from pyfondy.configuration import __version__

desc = """
    Fondy python sdk. 
    Docs   - https://docs.fondy.eu/
    README - https://github.com/cloudipsp/python-sdk/blob/master/README.md
  """

requires_list = [
    'six',
    'httpx'
]

setup(
    name='pyfondy',
    version=__version__,
    url='https://github.com/whiteapfel/pyfondy/',
    license='MIT',
    description='Python SDK for pyfondy clients.',
    long_description=desc,
    author='WhiteApfel, Dmitriy Miroshnikov',
    packages=find_packages(where='.', exclude=('tests*',)),
    install_requires=requires_list,
    classifiers=[
        'Environment :: Web Environment',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ])
