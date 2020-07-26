!#/bin/bash

gunicorn server:app -b 0.0.0.0:5000 -w 2 -t 5 --preload --access-logfile /tmp/gunicorn-access.log --error-logfile /tmp/gunicorn-error.log