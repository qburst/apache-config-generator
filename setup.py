import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-server-config-generator',
    url='https://github.com/Afsal-qburst/django-server-config-generator',
    version='0.6',
    packages=find_packages(),
    include_package_data=True,
    description='A simple Django app to create server config',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Afsal Salim',
    author_email='afsals@qburst.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)