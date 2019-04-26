from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name='Corvus',

    version='1.0.0',

   
    description='A binary data visualization tool.',

    long_description=long_description,

    long_description_content_type='text/markdown', 

    url='https://github.com/aaron-boyd/Corvus',


    author='Aaron Boyd',

 
    author_email='boydaaron06@gmail.com',

    classifiers=[

        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Binary Visualization :: Reverse Engineering',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],


    keywords='',

    #packages=['hexdump', 'matplotlib', 'PyQt5'],

    install_requires=['hexdump', 'matplotlib', 'PyQt5'],

    python_requires='>=3.0, <4',

    project_urls={ 
        'Github': 'https://github.com/aaron-boyd/Corvus',

    },
)

