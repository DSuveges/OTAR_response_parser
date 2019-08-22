from distutils.core import setup

# This script defines the installation and packaging properties for the python packages
# included in this repository

setup(
    name='OTAR_result_parser',
    version='0.1',
    include_package_data=True,
    packages=['OTAR_result_parser'],
    entry_points={
        "console_scripts": ['OTAR_result_parser = OTAR_result_parser:main']
    },
    url='https://github.com/dsuveges/OTAR_result_parser',
    license='',
    author='Daniel Suveges',
    author_email='dsuveges@ebi.ac.uk',
    description='Package that parses \'opentargets.conn.IterableResult\' objects.',
    install_requires=['pandas', 'pytest-cov', 'opentargets', 'coverage', 'codacy-coverage']
)
