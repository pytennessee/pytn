pytn
====

Getting Started:

    pip install virtualenv
    virtualenv --no-site-packages pytnenv
    source pytnenv/bin/activate
    git clone git@github.com:pytn/pytn.git pytn
    cd pytn
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py loaddata fixtures/*
    python manage.py runserver
