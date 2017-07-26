manage.py
=========

Automatic generation of a command line interface given Python function definitions.

`manage.py` tries to be as helpful as possible. It includes help messages based on doc-comments, usage strings generated from  argument lists (including positional and keyword arguments), and generally tries to leverage Python's dynamic and reflective features.

**Note:** manage.py is not meant to generate a CLI for an end user of a normal app. It is intented to create a simple programmer/admin friendly interface to control a stateful (web) application.

As an example of a `manage.py` file for a Flask web application

````python
#!/usr/bin/env python

import project

def runserver():
    """ Start the server """

    project.config.validate()
    project.run()

def createdb(drop=False):
    """
    Create the tables needed to run the application

    If drop is True, then all tables will first be dropped. THIS DESTROYS ALL
    DATA IN THE DATABASE.
    """

    if drop:
        project.db.drop_all()

    project.db.create_all()

def mkstaff(email, password, fname, lname, utype='staff'):
    """
    Create a new staff user

    This user will be able to access /admin routes and edit things. By
    default, creates a 'staff' user, not an 'admin'.
    """

    staff = User(email, password, fname, lname, utype)
    project.db.add(staff)
    project.db.commit()

################
# Caution: Magic
#
# Rest of file truncated...
````

If `manage.py` is run, the following output will be generated

````
Usage: manage.py [help] command [args...]
    createdb    Create the tables needed to run the application
    mkstaff     Create a new staff user
    runserver   Start the server
````

Running `manage.py mkstaff`, which is invalid due to missing required arguments, or running `manage.py help mkstaff` displays

````
Usage manage.py mkstaff <email> <password> <fname> <lname> [utype=staff]

    Create a new staff user

    This user will be able to access /admin routes and edit things. By
    default, creates a 'staff' user, not an 'admin'.
````

For functions like `mkstaff`, an arg spec is automagically generated, with required arguments displayed as `<arg-name>` and optional arguments as `[name=default-value]`.
