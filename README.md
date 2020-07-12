# Estimate Tax

## Source checkout
```
git clone https://github.com/ksranjith786/estimate-tax.git
cd estimate-tax
```
## Compilation Steps

### Creates a virtual env
```
python -m venv venv
```
Note: _If virutal environment **venv** not available then install it using **python -m pip venv**_

### Switch/Activate to venv
```
source venv/Scripts/activate
```

### Install the Python modules
```
pip install -r requirements.txt
```

## Execution Steps
```
export FLASK_APP=project
export FLASK_ENV=development
flask run
```

## Initial Steps
```
python -m venv venv
source venv/Scripts/activate
python -m pip install flask
python -m pip install gunicorn
python -m pip freeze > requirements.txt
```