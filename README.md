# Bong

[![Build Status](https://travis-ci.org/weedlabs/bong.png?branch=master)](https://travis-ci.org/weedlabs/bong)

Flask application scaffolding, modularized and 100% covered by unit
and functional tests; ready for extreme programming.

## Features

* SQLAlchemy support
* Simple ORM
* Command-line helpers through [flask-script](http://flask-script.readthedocs.org/)
* Easily create **application modules** *(analog to django apps)* through blueprints.
* WSGI container that sets up the plugins and blueprints
* Unique test DSL that looks turns writing tests into a more pleasant experience.
* Documentation support through [markment](http://falcao.it/markment)


## Getting Started in 5 steps

 1. Fork the project
 2. Clone from your own copy
 3. Run the `install-wizard.sh` script, which will install the dependencies in your environment
 4. Run the tests to make sure everything went well
 5. Disco!

## Bonus: Demo site

 1. Install [NPM](http://npmjs.org)

```bash
npm install bower
```

 2. Download and copy static files

```bash
make static
```

 3. Run the server

```bash
make run
```

 4. Disco!

![screenshot.png](screenshot.png)
