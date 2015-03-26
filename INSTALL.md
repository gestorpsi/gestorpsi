# GestorPsi install instructions
##Must have packages
These packages are installed using your distro package manager, remember that these names may vary depending on the distro you're using:
- python
- python-pip
- python-dev
- mariadb-server # or mysql-server
- libmariadbclient-dev # or libmysqlclient-dev
- libssl-dev

##Should have packages
These packages are installed through Python package manager aka pip:
```bash
$ sudo pip install virtualenvwrapper
```

###Configure recommended environment
In order to properly configure the environment, one must follow these steps:
```bash
$ echo 'source `which virtualenvwrapper.sh`' >> $HOME/.bashrc   # it adds virtualenvwrapper commands to bash
$ source $HOME/.bashrc  # don't need to reload bash session to have the commands available to you
$ mkvirtualenv gestorpsi    # creates a virtual environment(just like rvm does to Ruby and maven does to Java projects)
$ pip install ipython flake8    # it installs interactive python shell and flake8 code validation to your virtual environment
```
##Configure your database
To create the database that's going to be used, the command bellow must be executed:
```bash
$ mysqladmin create gestorpsi -u root
```
If you have set a password to your database, add the -p flag to be able to input your password

##Configure your settings.py
```bash
$ cd gestorpsi
$ cp settings.py.DIST settings.py
```

This is the part where you're going to change inside settings.py file(remember to set you username and password, if you have set one):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gestorpsi',             # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                 # Not used with sqlite3.
        'HOST': '',                 # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SERVER_EMAIL = '' # your email
DEFAULT_FROM_EMAIL = '' # your email
FROM_EMAIL = '' # your email

EMAIL_FROM = ''# your email
EMAIL_HOST = ''# your email host
EMAIL_HOST_USER = '' # your email
EMAIL_HOST_PASSWORD = '' # your email password
EMAIL_HOST_PORT = 587 # 465 or 587
EMAIL_USE_TLS = True

# Development environment only, comment this if you're going to use this in production environment
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend' # change way to write email instead of sending to the real email it writes to file
EMAIL_FILE_PATH = '/tmp/gestorpsi-emails' # change this to a proper location or create this folder, since it's going to be the folder where the emails are going to be written
```

###Creating emails folder
```bash
$ mkdir /tmp/gestorpsi-emails # or the name you want to
$ chmod ugo+rwx /tmp/gestorpsi-emails # dangerous move, but no need to worry here
```

##Installing project requirements
Make sure you're inside GestorPsi's virtualenv
```bash
$ workon gestorpsi # or the name of the env you have set
$ pip install -r requirements.txt
```
##Configuring project
```bash
$ python manage.py syncdb
$ python manage.py migrate
$ cd scripts
$ python creategroups.py
$ cd ..
$ python manage.py shell
```

This part you're going to type it inside the opened python interactive shell
```python
from gestorpsi.gcm.models.payment import *
p = PaymentType()
p.id = 1
p.name = 'Teste 1'
p.save()

p  = PaymentType()
p.id = 4
p.name = 'Teste 4'
p.save()
PaymentType.objects.all()
# output -> [<PaymentType: Teste 1>, <PaymentType: Teste 4>]
```

##Running server and executing system
```bash
$ python manage.py runserver
```
###Steps to follow after creating your account
- add service
- add service to professional
- add client
- subscribe client to service
