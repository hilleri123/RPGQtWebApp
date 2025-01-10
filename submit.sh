#!/bin/bash
rm resources_rc.py; pyrcc5 resources.qrc -o resources_rc.py;
alembic stamp head ; alembic revision --autogenerate -m "migration $(date +'%Y%m%d_%H%M%S')"
 ; alembic upgrade head ;
git add dialogs/*.py widgets/*.py common/*.py web_app/*.py web_app/templates/*.html web_app/static/* icons/*.png alembic/*.py alembic/versions/*.py ; git commit -am "a" ; git push origin master;

