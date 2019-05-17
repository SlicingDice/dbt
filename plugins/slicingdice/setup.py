#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

package_name = "dbt-slicingdice"
package_version = "0.0.1"
dbt_version = "0.14.0a1"
description = """The slicingdice adpter plugin for dbt (data build tool)"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author='SlicingDice',
    author_email='help@slicingdice.com',
    url='https://www.slicingdice.com',
    packages=find_packages(),
    package_data={
        'dbt': [
            'include/slicingdice/dbt_project.yml',
            'include/slicingdice/macros/*.sql',
        ]
    },
    install_requires=[
        'dbt-core=={}'.format(dbt_version),
        'pyodbc==4.0.26'
    ]
)
