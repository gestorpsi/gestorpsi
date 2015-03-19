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
    $ sudo pip install virtualenvwrapper

###Configure recommended environment
In order to properly configure the environment, one must follow these steps:
    - echo 'source `which virtualenvwrapper.sh`' >> $HOME/.bashrc   # it adds virtualenvwrapper commands to bash
    - source $HOME/.bashrc  # don't need to reload bash session to have the commands available to you
    - mkvirtualenv gestorpsi    # creates a virtual environment(just like rvm does to Ruby and maven does to Java projects)
    - pip install ipython flake8    # it installs interactive python shell and flake8 code validation to your virtual environment

##Configure your database
To create the database that's going to be used, the command bellow must be executed:
    - mysqladmin create gestorpsi -u root
If you have set a password to your database, add the -p flag to be able to input your password

##Configure your settings.py
    - cd gestorpsi
    - cp settings.py.DIST settings.py


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


SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
FROM_EMAIL = ''

EMAIL_FROM = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_PORT = 587 # 465 or 587
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/gestorpsi-emails' # change this to a proper location

##
cd <root gestorpsi>
pip install -r requirements.txt
./manage.py syncdb
./manage.py migrate

cd scripts
./creategroups.py

cd ..
./manage.py shell
- colar código:

from gestorpsi.gcm.models.payment import *
p  = PaymentType()
p.id = 1
p.name = 'Teste 1'
p.save()

p  = PaymentType()
p.id = 4
p.name = 'Teste 4'
p.save()
PaymentType.objects.all()


# output [<PaymentType: Teste 1>, <PaymentType: Teste 4>]

- - - saia do console

./manage.py runserver

- - - fazer registro como nova organização
cadastrar um servico
adicionar o servico ao professional
cadastrar um cliente
inscrever o cliente em um serviço (Nova Inscrição) barra lateral na direita
agenda disponível
