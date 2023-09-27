# test_task_image_storage DOCS

## Introduction

this is a test project in which is realized ability to upload images, get links to it and get expired links

## Features

- customized user tiers
- ability to work ith links
- JWT authorization

## How to use

### Installation

1. Clone the repository
2. `docker-compose up --build`
3. `python dataloader.py`(this will load build-in tiers and create users, one for each tier)
4. open http://0.0.0.0:8000 for the backend

## Backend

After instalation you will have 3 user(usernames: basic, premium, enterprise; passwords for all are 1234)
To log-in send a POST request to `http://0.0.0.0:8000/api/login/` with fields username and password, and you will get access and update tokens
You can refresh token on `http://0.0.0.0:8000/api/login/refresh/`
With tokens you will have access to app
### Endpoints(required header Authorization: Bearer {`access token`})
1.`api/v1/img` : handle GET and POST requests
on GET request you will get list of links to your images
POST handle image upload(required fields for POST: name, image_file)


2.`api/v1/img/<int:pk>` handle POST request, allow to create expiring link(only for users with certain ability)(required field: expiration_time)
it will return a expiration link which will redirect you to a image, and last for provided amount of seconds

