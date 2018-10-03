import setuptools

setuptools.setup(
    name="aws_py_the_urge",
    version="0.1.0",
    url="https://github.com/the-urge-tech/aws-py-the-urge.git",
    author="the urge",
    author_email="pierre.caserta@gmail.com",
    description=
    "An opinionated, minimal cookiecutter template for Python packages",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
