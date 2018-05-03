python3 manage.py makemigrations metadata
python3 manage.py migrate metadata
python3 manage.py makemigrations filing
python3 manage.py migrate filing
python3 manage.py enter_yearly_submissions 2016
#python3 manage.py enter_yearly_submissions 2016 --enter
python3 manage.py generate_schemas_from_metadata
python3 manage.py makemigrations return
python3 manage.py migrate return
