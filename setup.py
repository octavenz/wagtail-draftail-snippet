# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

readme = ""
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")

setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    name="wagtail-draftail-snippet",
    version="0.4.4",
    description="Associate RichTextBlock text content to a snippet model.",
    python_requires="==3.*,>=3.6.0",
    project_urls={
        "repository": "https://github.com/themotleyfool/wagtail-draftail-snippet"
    },
    author="Parbhat Puri",
    author_email="me@parbhatpuri.com",
    packages=["wagtail_draftail_snippet"],
    package_dir={"": "."},
    package_data={
        "wagtail_draftail_snippet": [
            "static/wagtail_draftail_snippet/js/*.js",
            "templates/wagtail_draftail_snippet/*.html",
        ]
    },
    install_requires=["wagtail>=2.15.0,<6.0"],
    extras_require={
        "dev": [
            "black==19.*,>=19.10.0",
            "flake8==3.*,>=3.7.9",
            "pytest==3.*,>=3.0.0",
            "pytest-django==3.*,>=3.8.0",
            "pytest-pythonpath==0.*,>=0.7.3",
            "wagtail-factories==2.*,>=2.0.0",
        ]
    },
)
