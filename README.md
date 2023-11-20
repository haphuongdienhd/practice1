# A basic Django exercises

## Practice 1: Django

1. Build a simple Django template app including these features

- Database: Postgres

- Create 2 apps

User

Catalog

2. Require:

- User App

Authentication

Local account

Social Account (Google, FB, Linkedin, etc, ..) => Optional

Sign-up new user

- Catalog App

CRUD Category

Pagination

Upload image

Tree

CRUD Product

Pagination

A product can belong to one or more categories

Can upload many images

Create product thumbnail

- Django Admin

Setup Django Admin for all models

Config filter, sort, queryset

Config edit field for foreign key if table has many records (raw_id_field)

## Practice 2: DRF

In the same project, implement APIs for User App and catalog App

Quickstart (https://www.django-rest-framework.org/tutorial/quickstart/)

Token Authentication

Sign up API

Category API

Product API

Product comments

Report APIs

Total of product per category

Total views of a product

Total comments of a product

Use swaggers for API documentation

## Practice 3: Celery

1. Add a new App (worker) and config Celery with Redis broker

2. Implement a celery task to send confirmation email after user signed up
Create a custom signal (user_signed_up)

3. Celery beat

- DB health check (run every minute) If failed => Send email to Admin

- Send an email to let Admin the list of users signed up during the day..
