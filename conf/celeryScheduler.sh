#!/bin/bash

cd /home/nfs/sharesWeb
celery -A sharesWeb.celery beat -l info -S django
