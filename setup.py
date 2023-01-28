from setuptools import setup

setup(
    name='safetypes',
    version='0.1rc2',
    packages=['safetypes', 'safetypes/base'],
    url='https://github.com/wiscot/safetypes',
    license='MIT',
    author='Rafael Gutiérrez Martínez',
    author_email='ragutimar@gmail.com',
    description='Python is a non typed language, and runs under the paradigm of first try and then '
                'it success or fails. This package allows you to have the capability of apply typing features '
                'in last versions of Python, allowing to the developer to have a transparent mechanism '
                'to grant that typing annotations are satisfied in the execution time of their programs.',

)
