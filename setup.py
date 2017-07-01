from setuptools import setup, find_packages

setup(
    name='pycno',
    description='A paste service, that doesn\'t track you',
    version='1.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires={
        'Flask==0.11.1',
        'Flask-WTF==0.14.2',
        'Pygments==2.1.3',
        'mulli==0.0.8-dev'
    },
)
