import setuptools
import pkg_resources

setuptools.setup(
    name="aws_py_the_urge",
    version="3.0.0",
    url="https://github.com/the-urge-tech/aws-py-the-urge.git",
    author="the urge",
    author_email="pierre.caserta@gmail.com",
    description="An opinionated, minimal cookiecutter template for Python packages",
    long_description=open("README.md").read(),
    packages=setuptools.find_packages(),
    package_data={"": ["*.json", "*.yaml"],},
    install_requires=["boto3", "python-slugify"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
