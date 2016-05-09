Django: Onder de Motorkap
=========================

This is the project for the http://djangoonderdemotorkap.nl/ website.


Development setup
-----------------

This project uses Python 3.5. Be sure to work within
`virtual environment <https://virtualenv.pypa.io/en/latest/>`_,
it will make your life easier. With virtualenv activated, install packages
as normal with ``pip install -r requirements.txt``.

This project uses `less <http://lesscss.org/>`_ for styles and so you'll
need `Node <https://nodejs.org/en/>`_ installed on your development machine.
After making sure you have node, install required npm packages
with ``make build-npm``.

There's a shortcut available that installs Python and Node dependencies::

    make build


Deploying
---------

Code is automatically deployed from ``master`` branch of this repository.


Deploying the old website
-------------------------

Say you need to deploy a new commit to the old website 2014.djangounderthehood.com.

Assuming:

* You have push access to the app on Heroku
* Your heroku git remote for the app is called `heroku-2014`

Here's what you do:

* Do your commit in the branch `oldsites/2014`
* `git push heroku-2014 oldsites/2014:master`
* ???
* Profit.
