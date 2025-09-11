#!/bin/bash
celery -A mate worker -E -l info --autoscale=5,1 -n celery_worker_%h