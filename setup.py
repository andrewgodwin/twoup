import os

from setuptools import find_packages, setup

# We use the README as the long_description
readme_path = os.path.join(os.path.dirname(__file__), "README.rst")
with open(readme_path) as fp:
    long_description = fp.read()

setup(
    name='twoup',
    version="1.0",
    url='https://github.com/django/daphne',
    author='Andrew Godwin',
    author_email='andrew@aeracode.org',
    description='SVG presentation tools',
    long_description=long_description,
    license='BSD',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Pillow',
        'pywinauto',
    ],
    entry_points={'console_scripts': [
        'twoup = twoup.cli:CommandLineInterface.entrypoint',
    ]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
    ],
)
