#!/bin/sh

if [ "$APPLY_MIGRATION" = 1 ] ; then
     alembic upgrade head
else
     python -m main
fi
