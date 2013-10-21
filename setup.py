from setuptools import setup, find_packages

# To install the twilio-python library, open a Terminal shell, then run this
# file by typing:
#
# python setup.py install
#
# You need to have the setuptools module installed. Try reading the setuptools
# documentation: http://pypi.python.org/pypi/setuptools
REQUIRES = ["xmlrpclib", "nose"]
TEST_REQUIRES = ["mock"]
setup(
    name = "testlink-python-api",
    version = "0.1",
    description = "TestLink Python client API",
    author = "Andrew Adams",
    author_email = "adamsar@gmail.com",
    url = "https://github.com/adamsar/testlink-python-api",
    keywords = ["testlink", "python"],
    install_requires = REQUIRES,
    tests_require = TEST_REQUIRES,
    packages = ['testlink'],
    package_dir = {'testlink': 'src/testlink'},
    include_package_data=True,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Test Management",
        ],
    long_description = """ """
    )
