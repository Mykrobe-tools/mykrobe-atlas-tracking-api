# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Tracking API",
    author_email="",
    url="",
    keywords=["OpenAPI", "Tracking API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    &lt;p&gt;An API for CRUD of sample tracking information for Mykrobe Atlas project &lt;p&gt;This API is intended to satisfy the following user stories &lt;li&gt; Atlas user wants to know the sample status so that I can know if specific results are available &lt;li&gt; Atlas user wants to know QC results for a sample so that I can know if a specific sample has passed QC check &lt;li&gt; Atlas user wants to deprecate a sample so that it is no longer available from the Atlas system &lt;li&gt; sample ingestion service wants to know if a sample already exists so that I can decide on rejecting a sample &lt;li&gt; sample ingestion service wants to know if a file already exists so that I can know if this is a new file &lt;li&gt; sample ingestion service wants to add a new sample for tracking so that It can know if the sample is accepted &lt;li&gt; sample processing service wants to add a processing event for a new sample so that the sample can be auditted &lt;li&gt; sampel processing service wants to add QC results for a new sample so that other user can know if the new sample passes the QC check &lt;li&gt; sampel processing service wants to update sample status so that they are up to date &lt;li&gt; sampel processing service wants to update sample&#39;s QC results so that they are up to date &lt;li&gt; audit user wants to know all the processing events for a sample so that I can know what happened to a sample
    """
)

