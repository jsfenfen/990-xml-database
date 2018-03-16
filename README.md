# 990-xml-database
Django app to consume and store 990 data and metadata. Depends on [IRSx](https://github.com/jsfenfen/990-xml-reader) (which is installed as a dependency below).

## Setup

1. git clone this repository `git clone https://github.com/jsfenfen/990-xml-database.git` and `$ cd 990-xml-database`

2. install the requirements with `pip install -r requirements.txt`. This is Django 2, so only python3 is supported.

3. copy the irsdb/local\_settings.py-example file to irsdb\/local_settings.py and edit it to reflect your database settings.

#### Adding the metadata

4. run `python manage.py makemigrations metadata` to generate the metadata migrations, and then run them with `python manage.py migrate metadata`.

5. Load the metadata with the management command: `python manage.py load_metadata`. This command erases the metadata before loading, so it can be rerun if it somehow breaks in the middle.

#### Adding index file data 

5.  run `python manage.py makemigrations filing` to generate the filing migrations, and then run them with `python manage.py migrate filing`.

6. Run `$ python manage.py enter\_yearly\_submissions \<YYYY\>` where YYYY is a the year corresponding to a yearly index file that has already been downloaded. { If it hasn't been downloaded you can retrieve it with irsx_index --year=YYYY } 

__Notes__ 

- enter\_yearly\_submissions: This is a management command that checks if the contents of the index files have been loaded previously, and only adds them if they haven't, so it can be rerun. It's not incredibly efficient though (it checks if each exists before deciding whether to load, although loading is done in bulk). It could be made to run faster if it stored a hash of known annual filings in memory while it ran, t
