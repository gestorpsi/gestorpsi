#  GestorPsi install instructions
 
 # # Must have packages  

These packages are installed using your distro package manager, remember that these names may vary depending on the distro you're using:
- python
-  python-pip
- python-dev
- mariadb-server # or mysql-server
- libmariadbclient-dev # or libmysqlclient-dev
- libssl-dev

## Should have packages

These packages are installed through Python package manager aka pip:

```bash
$ sudo pip install virtualenvwrapper
```

### Configure recommended environment

In order to properly configure the environment, one must follow these steps:

```bash
$ echo "source `which virtualenvwrapper.sh`" >> $HOME/.bashrc  # it adds virtualenvwrapper commands to bash
$ source $HOME/.bashrc  # don't need to reload bash session to have the commands available to you
$ mkvirtualenv gestorpsi    # creates a virtual environment(just like rvm does to Ruby and maven does to Java projects)
$ pip install ipython flake8    # it installs interactive python shell and flake8 code validation to your virtual environment
```

## Configure your database

To create the database that's going to be used, the command bellow must be executed:

```bash
$ mysqladmin create gestorpsi -u root
```
If you have set a password to your database, add the -p flag to be able to input your password

## Configure your settings.py

```bash
$ cd gestorpsi
$ cp settings.py.DIST settings.py
```

If your database has a password, make sure to put it on your settings.py in the DATABASES hash.

## Installing project requirements

Make sure you're inside GestorPsi's virtualenv

```bash
$ workon gestorpsi # or the name of the env you have set
$ pip install git+https://github.com/digi604/django-smart-selects.git@eea07eeb759f75c77497b2425b84574cf6c6ac4d
$ pip install -r requirements.txt
```

## Configuring project

```bash
$ python manage.py syncdb
$ python manage.py migrate
$ cp scripts/header.py.DIST scripts/header.py
$ ./scripts/install/createGroups.py
$ ./scripts/install/createAdmin.py
$ python manage.py shell
```

if the command ```bash python manage.py shell``` fails, you will need to update the package six that did not have the PY2 identifier.

```bash pip install --upgrade six```

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

## Enabling locale

In order to be able to execute the makemessages/compilemessages commando, you must enter the gestorpsi folder where the locale folder is a child

```bash
$ cd gestorpsi
$ python ../manage.py makemessages --all
$ python ../manage.py compilemessages
```

## Running server and executing system

```bash
$ python manage.py runserver
```

### Steps to follow after creating your account

- add service
- add service to professional
- add client
- subscribe client to service

