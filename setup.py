#! /usr/bin/env python3

import setuptools


with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name="guidtool",
    version="1.0",
    author="Daniel Thathcer",
    description="A tool for analysing and forging type 1 UUID/GUIDs",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": [
            "guidtool = guidtool:main"
        ]
    }
)
