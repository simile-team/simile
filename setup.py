import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simile",  # Replace with your desired package name
    version="0.1.1",
    author="Joon Sung Park",
    author_email="joon.s.pk@gmail.com",
    description="A Python client library for interacting with my Agent & Population endpoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simile-team/simile",  # or your repo link
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.22.0",
        "urllib3>=1.26.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your choice
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
