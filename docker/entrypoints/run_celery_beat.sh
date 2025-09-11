#!/bin/bash
celery -A mate beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler