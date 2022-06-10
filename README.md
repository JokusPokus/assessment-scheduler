# CODE Assessment Scheduler
This system was created by Jakob Schmitt ([@JokusPokus](https://github.com/JokusPokus))
as a Capstone Project at CODE University of Applied Sciences.

___


[![version](https://img.shields.io/badge/version-v1.0-6EB8D0)](https://github.com/JokusPokus/assessment-scheduler)
[![URL](https://img.shields.io/badge/URL-https%3A%2F%2Fexamsched--rbnh6rv7hq--ey.a.run.app%2F-blue)](https://examsched-rbnh6rv7hq-ey.a.run.app/)
![Build](https://github.com/JokusPokus/assessment-scheduler/actions/workflows/dev.backend.yml/badge.svg?branch=develop)
![Delivery Pipeline](https://github.com/JokusPokus/assessment-scheduler/actions/workflows/prod.backend.yml/badge.svg?branch=main)



The repository contains three components:
* the **backend**, which provides an API to manage assessment phases 
and trigger the planning process (deployed on Google Cloud)
* the **frontend**, which provides a web client to the examination office
 staff (served as an SPA via the API root route)
* the **terraform** specifications, which define the project's cloud architecture

This document aims to give an overview about the techstack and code structure. 
In addition, the reader gets to know how to install and setup a local development environment.

## Techstack
### Backend

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [JWT](https://jwt.io/)
- [pytest](https://docs.pytest.org/en/6.2.x/) (for development and testing)

### Frontend 

- [React.js](https://github.com/facebook/react)
- [AntDesign](https://github.com/ant-design/ant-design)


## Installation
Opening remark: To avoid confusion, please note that a local installation differs from the production version
in many ways. For example, you will find that in production, the UI is served 
as an SPA at the backend's API root route. However, if you follow the local
installation steps below, the frontend and API will be hosted at different ports,
respectively. 

Requirements:
* [Docker](https://docs.docker.com/get-docker/)

First, clone the respository:
```zsh
git clone https://github.com/JokusPokus/assessment-scheduler.git
cd ./assessment-scheduler
```

For your convenience, the whole ecosystem can be spun up with one single command:

```zsh
docker-compose up -d --build
```

This command will: 
* create a PostgreSQL container
* create a backend service
* migrate the database
* start the client and expose it on `localhost:8080` 

**After all three containers (`database`, `app`, `client`) have been started, 
wait for at least one minute to make sure the React app is properly started!**

To use the regular client at `localhost:8080` or the admin UI at `localhost:8000/admin/`,
you need to create a super user like this:

```zsh
docker-compose exec app python manage.py initadmin
```

This command will create a superuser with username "admin" and password "admin".

## Running tests

If you wish, you can run the test suite using this command:

```zsh
docker-compose exec app pytest
```

Note that appending `-m unit` specifically runs all unit tests.  


## Using the service

After the installation step is completed, you can access the regular
UI at `localhost:8080` and the Django admin UI at `localhost:8000/admin/`. You
can use the admin user (username: admin, password: admin). Further users
can be created via the Django admin interface.

Note: If the admin user is not found, you might have skipped the creation
step in the installation process.


## Shutting down the containers

When you're done exploring, you can shut down the docker containers like this:

```zsh
docker-compose stop
```

## Further information

Comprehensive project documentation (including architecture, cyber security,
planning & optimization algorithms used in the project) can be found in the repository wiki.
