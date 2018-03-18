# 990-xml-database
Django app to consume and store 990 data and metadata. Depends on [IRSx](https://github.com/jsfenfen/990-xml-reader) (which is installed as a dependency below).

## Setup

1. git clone this repository `git clone https://github.com/jsfenfen/990-xml-database.git` and `$ cd 990-xml-database`

2. install the requirements with `pip install -r requirements.txt`. This is Django 2, so only python3 is supported.

3. copy the irsdb/local\_settings.py-example file to irsdb\/local_settings.py and edit it to reflect your database settings.

#### Adding the metadata

1. run `python manage.py makemigrations metadata` to generate the metadata migrations, and then run them with `python manage.py migrate metadata`.

2. Load the metadata with the management command: `python manage.py load_metadata`. This command erases the metadata before loading, so it can be rerun if it somehow breaks in the middle.

#### Adding index file data 

1.  run `python manage.py makemigrations filing` to generate the filing migrations, and then run them with `python manage.py migrate filing`.

2. Run `$ python manage.py enter_yearly_submissions <YYYY>` where YYYY is a the year corresponding to a yearly index file that has already been downloaded. { If it hasn't been downloaded you can retrieve it with irsx_index --year=YYYY }. This script checks to see if the IRS' index file is any bigger than the one one disk, and only runs if it has. You can force it to try to enter any new filings (regardless of whether the file is updated) with the `--enter` option.

#### Generate the schema files - Not required

Run `$ python manage.py generate_schemas_from_metadata` to generate a django models file (to the directory generated_models). You can modify these and put them into return/models.

#### Create the return tables

This is just another migration, but it creates 180 tables. Django seems to spit out a lotta warnings, they don't seem to reflect actual problems? 
`$ python manage.py makemigrations return`
To make the migrations and   
`$ python manage.py migrate return`
to run them.

#### Load the filings

Actually enter the filings into the database with 
`$ python manage.py load_filings <YYYY>`. 

This script will take a while to run--probably at least several hours per year. You'll likely want to run it using nohup, so something like this:


`$ nohup python manage.py load_filings <YYYY> &`

Which detaches the terminal from the process, so if your connection times out the command keeps running.

You may want to adjust your postgres settings for better loading, but you'll need to pay attention to overall memory and resource uses. 




#### Analyze the load process

The loading process uses columns in the filing model to track load process (and to insure the same files aren't loaded twice). 

TK - explanation of keyerrors


#### Removing all rows

There's a [sql script](https://github.com/jsfenfen/990-xml-database/blob/master/irsdb/return/sql/delete_all_return.sql) that will remove all entered rows from all return tables and reset the fields in filing as if they were new. 

If you want to live dangerously, you can run it from the console like this:

`$ python manage.py dbshell < ./return/sql/delete_all_return.sql`


#### Adding or removing indexes

There are management commands to create or drop indexes on object\_id, ein and (for schedule K) documentId. Use
`$ python manage.py make_indexes` or 
`$ python manage.py drop_indexes` . These are just conveniences to create indexes named xx_\<tablename\> --they won't remove other indexes.

#### Removing a subset of all rows

You can remove all filings from a given index file with the [remove_year](https://github.com/jsfenfen/990-xml-database/blob/master/irsdb/return/management/commands/remove_year.py). It's likely to run faster if indexes are in place. 

#### Removing only the rows that were half loaded

If loading gets interrupted, you can remove only the rows where parse\_started is true and parse\_complete is not with the management command [remove\_half\_loaded](https://github.com/jsfenfen/990-xml-database/blob/master/irsdb/return/management/commands/remove_half_loaded.py). It also requires a year as a command line argument.
 
 `$ python manage.py remove_half_loaded 2018`

#### File size concerns

The full download of uncompressed .xml files is over ~74 gigabytes. Processing a complete year of data probably entails moving at least 15 gigs of xml. 

You probably want to look into a tool to help you move these files in bulk. AWS' S3 CLI can dramatically reduce download time, but seems unhelpful when trying to pull a subset of files (it seems like [--exclude '*'](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters) hangs when processing so many files). You may want to look into moving all the files to your own S3 bucket as well. There are also alternatives to AWS' CLI tool, like [S3 CMD](http://s3tools.org/s3cmd).

You'll also want to [set IRSx](linkTK) [link tk] to look for the xml files in whatever directory you downloaded them to.

The worst option is to download the uncompressed files one at a time. That sounds, really, really slow. 


#### Server considerations

With most hosting providers, you'll need to configure additional storage to support the static files and the database that's ultimately loaded. Make sure that you set the database storage directory to *that storage*, and get the fastest storage type you can afford.

You may want to look into tuning your database parameters to better support data loading. And you'll get better performance if you only create indexes after loading is complete (and delete them before bulk loads take place).

One random datapoint: on an Amazon t2.medium ec2 server (~$38/month) with 150 gigs of additional storage and postgres running on the default configs and writing to an SSD EBS volume, load time for the complete set of about 490,000 filings from 2017 took about 3 hours.