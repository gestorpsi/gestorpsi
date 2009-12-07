#!/bin/bash

echo ""
echo "Copyright (C) 2009 GestorPsi"
echo ""
echo "This program is free software; you can redistribute it and/or"
echo "modify it under the terms of the GNU General Public License"
echo "as published by the Free Software Foundation; either version 2"
echo "of the License, or (at your option) any later version."
echo ""
echo "This program is distributed in the hope that it will be useful,"
echo "but WITHOUT ANY WARRANTY; without even the implied warranty of"
echo "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
echo "GNU General Public License for more details."
echo ""
echo ""
echo "ATTENTION !!! ATTENTION !!! ATTENTION !!! ATTENTION !!! ATTENTION !!!"
echo ""
echo ""
echo "This is an EXPERIMENTAL script that try to update your GestorPSI SVN tree"
echo "to the last version making all of the necessary changes in your database"
echo ""
echo "If you are not secure to use this script, please read the UPDATING document"
echo "in the root folder of this project to procced with manually update"
echo ""
echo "If you really want proceed with this script, have sure you already have"
echo "BACKUP FROM YOUR DATABASE, and from your local copy as well"
echo ""
echo "You also must to have Subversion and Django-South installed"
echo ""
echo "Do you REALLY want to proceed (y/n)?"

read proceed

if [ ${proceed} != y ] && [ ${proceed} != Y ]
    then
    echo "Quiting..."
    exit 0
fi

echo "Do want want to migrate to an specific (v)ersion or updated to the (l)ast version available in the repository (v/l)? "
read migration_type

if [ ${migration_type} = v ] || [ ${migration_type} = V ]
    then
    echo "Which version? (eg.: 1080)"
    read version
fi

echo "Did you make backup from your database and your local copy (y/n)?"
read backup
if [ ${backup} != y ] && [ ${backup} != Y ]
    then
    echo "Quiting..."
    exit 0
fi

echo "Are you sure (y/n)?"
read sure
if [ ${sure} != y ] && [ ${sure} != Y ]
    then
    echo "Quiting..."
    exit 0
elif [ ${sure} = y ] || [ ${sure} = Y ]
    then
    array=(authentication util sponsor organization careprofessional contact place device service client admission referral phone address person employee document internet upload support cbo demographic ehr online_messages schedule)
    # clean update south table
    python util/reset_south.py

    # generate initial data model
    for i in ${array[*]}; do 
        rm -rf $i/migrations
        echo "Registering $i"; 
        python manage.py convert_to_south $i
    done

    # update sources
    if [ ${migration_type} = v ] || [ ${migration_type} = V ]
    then
        svn up -r${version}
    else
        svn up
    fi

    # generate new models
    for i in ${array[*]}; do
            echo "Updating $i";
            python manage.py startmigration $i last --auto
    done

    # commit database
    for i in ${array[*]}; do
            echo "Commiting $i";
            python manage.py migrate $i 0002_last
    done
    echo "Upgrade Completed."
fi
