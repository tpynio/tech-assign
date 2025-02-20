#!/bin/sh

if [ "$APPLY_MIGRATION" = 1 ] ; then
    alembic upgrade head
elif [ "$CELERY_BEAT" = 1 ] ; then
    celery -A periodic.celerybeatSchedule beat
elif [ "$CELERY_WORKER" = 1 ] ; then
    celery -A periodic.tasks worker
else
    python -m main
fi
