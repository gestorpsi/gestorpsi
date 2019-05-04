gestorpsi
=========

Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.


----------------------------------
GestorPsi - Psychology Services Management System
----------------------------------

![build](https://travis-ci.org/gestorpsi/gestorpsi.svg?branch=master)


About
-----
GestorPsi is a system to management one, or many clinic organizations.
It was developed using Python 2.5 language, Django framework
(www.djangoproject.com) and JQuery (www.jquery.com)


Features
--------
The basic features of GestorPsi are:
- Organization Profile
- Customers Management
- Profesionals Management
- Services Management
- Places Management
- Rooms Management
- Contacts Management
- Employees Management
- Devices Management
- UUid
- Encrypted Database (see: crypt_howto.txt)


Todo
--------
- Schedule
- Reports


Quick Install (with docker)

------------
Just run:

> $ docker-compose up

Then go to http://127.0.0.1:8000 in your browser

Note:
You must to have docker-compose installed before.
For more information, please visit https://docs.docker.com/compose/install/


Manual installation
------------

After downloaded and extracted GestorPsi source files, installing
GestorPsi is done by the following:

1) export PYTHONPATH environment variable to your django project
dir.
Ex.: if your sources was extracted to /home/foo/gestorpsi
$ export PYTHONPATH="/home/foo/gestorpsi"

2) Change to project Directory
$ cd /home/foo/gestorpsi

3) Create database tables
$ python manage.py syncdb

4) Install default groups and users data
$ python install.py

5) Open settings.py and edit the follow config:
  -> DATABASE_NAME
        -> DATABASE_USER
        -> DATABASE_PASSWORD
        -> DATABASE_HOST
        -> DEBUG (set to False)
        -> MEDIA_URL
        -> MEDIA_ROOT
        -> SECRET_KEY
        -> TEMPLATE_DIRS
        -> EMAIL_HOST
        -> EMAIL_HOST_USER
        -> EMAIL_HOST_PASSWORD 

6) Compile language messages (optional)
$ django-admin.py compilemessages -a

7) Run development server
$ python manage.py runserver

8) Open your browser, and go to http://127.0.0.1:8000/

If there are any errors during installing, check your build environment
and try to find the error, otherwise contact one of the authors.


Requirements
------------
Before install GestorPsi, you need to get and install the follows
Python packages:

- Python (>=2.5)
  maintainer: http://www.python.org/

- Python Imaging Library (PIL)
  maintainer: http://www.pythonware.com/products/pil/
  debian/ubuntu: sudo apt-get install python-imaging

- Python Cryptography Toolkit (>= 2.1.0)
  maintainer: http://www.pycrypto.org
  debian/ubuntu: sudo apt-get install python-crypto

- Python Dateutil (>= 1.3-1)
  debian/ubuntu: sudo apt-get install python-dateutil

- Django Swingtime (>= 0.2)
  maintainer: http://code.google.com/p/django-swingtime/

- Gettext (>= 0.17-2)
  debian/ubuntu: sudo apt-get install gettext

- Django Registration (>= 0.8)
  maintainer: http://bitbucket.org/ubernostrum/django-registration/wiki/Home

- Django Reversion (>= r197)
  maintainer: http://code.google.com/p/django-reversion/

- Django South (>= 0.6)
  maintainer: http://south.aeracode.org/

- Django Rosetta (>= 0.4.5)
  maintainer: http://code.google.com/p/django-rosetta/

- Some database server running, and configured:
  MySQL Server, PostgreSQL, Oracle or SQLite

- Python module for PostgreSQL
  debian/ubuntu: sudo apt-get install python-psycopg2

- Pisa (>= 3.0.32)
  maintainer: http://pypi.python.org/pypi/pisa/
  debian/ubuntu: sudo apt-get install python-pisa

- html5lib (>= 0.11.1-1)
  debian/ubuntu: sudo apt-get install python-html5lib
  
- pygooglechart (revision 67)
  http://pygooglechart.slowchop.com/

- Firefox Web Browser (>=3.0.5)
  maintainer: http://www.mozilla.com/firefox/


License
-------
GestorPsi is distributed under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.  A copy of this license
can be found in the file COPYING included with the source code of this
program.

Ideas, questions, patches and bug reports
support@gestopsi.com.br

--
2007-2009 by GestorPsi
www.gestorpsi.com.br
