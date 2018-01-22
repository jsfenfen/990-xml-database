# 990-xml-database
Django app to consume and store 990 data and metadata. Depends on [irsx](https://github.com/jsfenfen/990-xml-reader) (which is installed as a dependency below).

## Setup

1. git clone this repository `git clone https://github.com/jsfenfen/990-xml-database.git` and `$ cd 990-xml-database`

2. install the requirements with `pip install -r requirements.txt`. This is Django 2, so only python3 is supported.

3. copy the irsdb\/local\_settings.py-example file to irsdb\/local_settings.py and edit it to reflect your database settings.

4. run `python manage.py makemigrations metadata` to generate the metadata migrations, and then run them with `python manage.py migrate metadata`.

5. Load the metadata with the management command: `python manage.py load_metadata`. This command erases the metadata before loading, so it can be rerun if it somehow breaks in the middle.

