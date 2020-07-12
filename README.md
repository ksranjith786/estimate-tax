python -m venv venv
source venv/Scripts/activate
python -m pip install flask
python -m pip install gunicorn
python -m pip freeze > requirements.txt


$ export FLASK_APP=project
$ export FLASK_ENV=development
$ flask run