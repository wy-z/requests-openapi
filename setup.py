import io
import os

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return fd.read()


setup(
    name="requests-oai",
    url="https://github.com/wy-z/requests-oai",
    license="MIT",
    author="weiyang",
    author_email="weiyang.ones@gmail.com",
    description="OAIRequest is a python client library for OpenAPI 3.0",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests", "pyyaml"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
