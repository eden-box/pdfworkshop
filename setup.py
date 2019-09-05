#! usr/bin/env python3.7

from setuptools import setup, find_packages

__application__ = 'pdfworkshop'
__version__ = '1.0.3'

setup(
    name=__application__,

    python_requires='~=3.5',

    version=__version__,

    description='PDF compressor utility, using iLovePDF API',

    long_description=open('README.md', 'r').read(),

    long_description_content_type='text/markdown',

    url='https://github.com/eden-box//{}'.format(__application__),

    author='Eden-Box',

    author_email='eden.box@outlook.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Topic :: Office/Business',
    ],

    keywords='python pdf compress ilovepdf',

    scripts=[],

    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'click',
        'appdirs',
        'pylovepdf',
    ],

    tests_require=[
    ],

    extras_require={
        'dev': [
            'wheel',
        ]
    },

    entry_points={
        'console_scripts': [
            '{}=pdfworkshop.cli:start'.format(__application__),
        ],
    },
)
