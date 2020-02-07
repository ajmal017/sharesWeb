#!/bin/bash

NAME="sharesWeb"                                  # Name of the application
DJANGODIR=/home/nfs/sharesWeb             # Django project directory
SOCKFILE=/tmp/sharesWebGu.sock  # we will communicte using this unix socket
USER=root                                        # the user to run as
GROUP=root                                     # the group to run as
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spaw
DJANGO_SETTINGS_MODULE=sharesWeb.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=sharesWeb.wsgi                     # WSGI module name

# echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/nfs/sharesWeb/sharesweb/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
#exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=127.0.0.1:8288 \
  #--max-requests=1 \
  --log-level=debug \
  --log-file=/home/tmp/gunicornSharesWeb.log
