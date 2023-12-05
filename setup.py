from setuptools import setup, find_packages
from json_relational import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="json_relational",
      version=__version__,
      author="gr0vity",
      description="convert nested json to flat objects and their mapping",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/gr0vity-dev/json-relational",
      packages=find_packages(exclude=["unit_tests"])
      )
