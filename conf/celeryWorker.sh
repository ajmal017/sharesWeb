#!/bin/bash

cd /home/nfs/sharesWeb
celery -A sharesWeb.celery worker -l info
