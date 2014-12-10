from fabric.api import *
from fabric.colors import green, red

def server() :
    """This pushes to the EC2 instance defined below"""
    # The Elastic IP to your server
    env.host_string = '104.131.169.98'
    # your user on that system
    env.user = 'gestorpsi'
    env.password = 'gestorpsi'
    # Assumes that your *.pem key is in the same directory as your fabfile.py
    # env.key_filename = '104.131.169.98.pem'

def staging() :
    # path to the directory on the server where your vhost is set up
    path = "/srv/www/gestorpsi"
    # name of the application process
    process = "apache2"

    print(red("Beginning Deploy:"))
    with cd("%s" % path) :
        run("pwd")
        print(green("Pulling master from GitHub..."))
        run("git pull origin fabric")
        print(green("Installing requirements..."))
        run("pip install -r requirements.txt")
        print(green("Collecting static files..."))
        run("python manage.py collectstatic --noinput")
        print(green("Syncing the database..."))
        run("python manage.py syncdb")
        print(green("Migrating the database..."))
        run("python manage.py migrate")
        print(green("Restart the uwsgi process"))
        sudo("service %s restart" % process)
    print(red("DONE!"))