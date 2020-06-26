aws-py-the-urge
===============

# change the version in >>>>> setup.py <<<<<<

To update the module in other project:

# change the sha in pipenv
```
pipenv update aws-py-the-urge
pipenv lock -r > requirements.txt
```

To get the last version locally (if not using pipenv)
```
pip install --force-reinstall -r requirements.txt
```

To check your local version
```
pip show aws-py-the-urge
# check version
```

# Packages using this library
- enricher 
- feeds-dl 
- image-downloader
- fetcher 
- ingester 

# run tests
```
cd aws_py_the_urge
nosetests tests/
```



```

for i in * 
do
echo "$i=`cat $i`" 
done
```
