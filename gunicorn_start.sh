#!/bin/bash

# Check if sudo
if [[ $(id -u) -ne 0 ]]; then
    echo "Please run as root" && exit 1
fi

SITENAME="www.lyzer.com"
DJANGODIR=~/sties/$SITENAME/source
SOCKFILE=~/sites/$SITENAME/run/gunicorn.sock
USER=$('whoami')
GROUP=lyzer
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=lyzer.settings
DJANGO_WSGI_MODULE=lyzer.wsgi

echo "Starting $SITENAME as `whoami`"

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start Django Unicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $SITENAME \
    --workers $NUM_WORKERS \
    --worker-class gevent \
    --user=$USER --group=$GROUP \
    --bind=127.0.0.1:8000 \
    --log-level=debug
#--log-file=-