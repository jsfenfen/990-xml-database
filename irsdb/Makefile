export IRSX_CACHE_DIRECTORY=.

YEARS = 2014 2015 2016 2017 2018 2019

all : $(patsubst %,filing_%,$(YEARS))

initialize_db :
	python manage.py makemigrations metadata
	python manage.py migrate metadata
	python manage.py load_metadata
	python manage.py makemigrations filing
	python manage.py migrate filing
	python manage.py makemigrations return
	python manage.py migrate return
	touch $@

.PRECIOUS : $(patsubst %,CSV/index_%.csv,$(YEARS))
$(IRSX_CACHE_DIRECTORY)/CSV/index_%.csv : initialize_db
	python manage.py enter_yearly_submissions $*

irs-990-form/CSV/index_2014.csv : initialize_db
	wget -O $@ -N https://s3.amazonaws.com/irs-form-990/$(notdir $@)
	perl -i.bak -p -e 's/SILVERCREST ASSET ,AMAGEMENT/SILVERCREST ASSET MANAGEMENT/g' $@
	python manage.py enter_yearly_submissions 2014

download_filings_% :
	aws s3 sync s3://irs-form-990 $(IRSX_CACHE_DIRECTORY)/XML --exclude "*" --include "$**.xml" --no-progress | pv -l > /dev/null

filing_% : $(IRSX_CACHE_DIRECTORY)/CSV/index_%.csv download_filings_%
	python manage.py load_filings $* 

