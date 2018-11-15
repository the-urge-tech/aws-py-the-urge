aws-py-the-urge
===============

To update the module in other project:
```
# change the version in __init__.py
# change the version in setup.py <<<<<<<<<---
# change the sha in pipenv

pipenv update aws-py-the-urge
pipenv lock -r > requirements.txt
```

To get the last version locally
```
pip install --force-reinstall -r requirements.txt
```

To check your local version
```
pip show -f aws-py-the-urge
# check path
# go look for the version
```
