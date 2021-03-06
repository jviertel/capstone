# PedalsDB API

## Introduction

The PedalsDB API is a simple API designed to provide data from a centralized database of guitar pedal and guitar pedal manufacturers. For those who are not familiar with guitar, guitar pedals are small electronic boxes that your electric guitar's sonic signal chain runs through. They change different aspects of your guitar sound as the signal runs through the electronics of the pedal. There are many different ways in which guitar pedals (or stompboxes as they are also called) change a guitar's sound. One type of pedal is the distortion pedal, which intentionally degrades the signal to produce harder guitar sounds. Another type of pedal is the reverb pedal, which simulates the the accoustics of different spaces artificially. Most anyone that is into playing guitar, either collects or has used and is familiar with guitar pedals. 

That's why I created this guitar pedals API. A few months ago, I started hand cataloging pedals into Excel spreadsheets because I wanted to learn more about the various pedals and manufacturers and explore price points. I have recently gained the skills necessary to make an API for that data through a Udacity nanodegree, so I decided to take the opportunity to create an API for that my data as a final project for that course. Currently, this project has no frontend, but will most likely have one in the future.

## Installation and Setup

This project uses a Python for the backend. Downloads for the latest version of Python for your OS can be found at https://www.python.org/downloads/

The Python package manage pip is also needed to install dependencies. It comes along with current Python installations, but may need to be upgraded to the most current version. Please visit https://pip.pypa.io/en/stable/installing/#upgrading-pip for more information on pip as needed. 

As wtih most Python projects, it is very helpful to have the dependencies in a virtual environment. Instructions for how to set up and activate a virtual environment can be found at the below link.

https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/


The requirements for the project are listed in the requirements.txt file. 

Run:

pip install requirement.txt


Testing this project also relies on a copy of the pedalsdb database. A copy can be created through use of the pedalsdb.psql dump file. This can be done by creating a database on your local machine, then running the pedalsdb.psql file.

CREATE DATABASE pedalsdb_test
psql pedalsdb_test < pedalsdb.psql

## Running
The app can be run using the commands below:

#### Windows

set FLASK_APP = app.py

set FLASK_ENV = development

flask run


#### Linux

export FLASK_APP = app.py

export FLASK_ENV = development

flask run


It is also hosted on Heroku at the url:

http://pedalsdb.herokuapp.com/

Note: As noted above, there is no frontend yet for this api, so please test using the steps provided below. 

## Models
Models for the database are in models.py. The model classes also contain methods for database actions used elesewhere in the codebase. The models are as follows:

#### Manufacturer

- id: primary key, auto increments, unique identifier for Manufacturer rows relates to the manufacturer_id column foreign key in the Pedals table

- name: string, name of the manufacturer

- website_link: string, url of the manufacturer's website

### Pedal

- id: primary key, auto increments, unique identifier for Pedal rows

- name: string, name of the pedal

- type: string, pedal effect type

- new_price: string, new price for the pedal, may be empty if pedal if not currently in production

- used_price: string, used price for pedal, may be empty if pedal is brand new or used price is not lower than new price

- manufacturer_id: foreign key, relates to id in Manufacturer table

## Testing
Unittests can be run on the app from the test_app.py file. To run the tests:

- Create database (in psql)

DROP DATABASE IF EXISTS pedalsdb_test

CREATE DATABASE pedalsdb_test

(from regular command line)
psql pedalsdb_test < pedalsdb.psql

- Run Tests

python test_app.py

Note: The test_app.py file contains tokens that are required for the tests to run correctly. The tokens are valid for 24 hours from when they were created. 

## API Endpoints

- GET /manufacturers
- GET /manufacturers/<manufacturer_id>/pedals
- POST /manufacturers
- POST /pedals
- PATCH /manufacturers/<manufacturer_id>
- PATCH /pedals/<pedal_id>
- DELETE /manufacturers/<manufacturer_id>
- DELETE /pedals/<pedal_id>

#### GET /manufacturers
- Public endpoint
- Gets all manufacturers
- Returns JSON with list of manufacturers, number of manufacturers, and success value

Note: For simplicity, one manufacturer listing is shown in the manufacturers array here and in all of endpoint exapmles so user can get the idea of what the representation of the manufacturer data looks like without cluttering the example. 
Example Return 

{'manufacturers': [{"id":4,"name":"BBE","website_link":"http://www.bbesound.com/"}], "num_manufacturers":3,"success":true}

#### GET /manufacturers/<manufacturer_id>/pedals
- Public endpoint
- Gets pedals for the given manufacturer_id
- Returns JSON with manufacturer id, name of manufacturer, pedals array for given manufacturer, num of pedals for manufacturer, and success value

Note: Again here, one pedal listing is shown in pedals array for simplicity, but to still convey what the data representation looks like
Example Return

{"manufacturer_id":4,"manufacturer_name":"BBE","num_pedals":2,"pedals":[{"id":1,"manufacturer_id":4,"name":"Soul Vibe SV-74","new_price":"$140.00","pedal_type":"Rotary Speaker Simulator","used_price":"$64.00"}],"success":true}

#### POST /manufacturers
- Requires post:manufacturers permission (held by the Contributor and Site Owner users)
- Creates new manufacturer
- Takes JSON with name of manufacturer and website link
-Prevents duplicate entries

Ex. 

{'name': 'Volcanic Audio', 'website_link': 'https://www.volcanicaudio.com'}

- Returns JSON with created manufacturer id, manufacturers array, number of manufacturers, and success value

Example Return

{'created_manufacturer': 53, 'manufacturers': [{"id":4,"name":"BBE","website_link":"http://www.bbesound.com/"}], 'num_manufacturers': 53, 'success':  True}

#### POST /pedals
- Requires post:pedals permission (held by Contributor and Site Owner users)
- Creates new pedal
- Takes JSON with name of pedal, pedal type, new price, used price, and manufacturer id
- Prevents duplicate entries

Ex. 

{'name': 'California Surf', 'pedal_type': 'Reverb', 'new_price': '$99.00', 'used_price': '$65.00', 'manufacturer_id': 37}

- Returns JSON with created pedal id, pedals array, number of pedals, and success value

Example Return

{'created_pedal': 847, 'pedals': [{"id":1,"manufacturer_id":4,"name":"Soul Vibe SV-74","new_price":"$140.00","pedal_type":"Rotary Speaker Simulator","used_price":"$64.00"}], 'num_pedals': 847, 'success': False}

#### PATCH /maufacturers/<manufacturer_id>
- Requires patch:manufacturers permission (held by Site Owner user)
- Updates manufacturer's data for manufacturer with manufacturer_id
- Takes JSON with manufacturer name and manufacturer website url

Ex. 

{'name': 'Changed Name','website_link': 'https://www.pedals.info.com'}

- Returns JSON with patched manufacturer's id, manufacturer array, number of manufacturers, and success value

Example Return

{'updated_manufacturer': 4, 'manufacturers': [{"id":4,"name":"BBE","website_link":"http://www.bbesound.com/"}], 'num_manufacturers': 56, 'success': True}

#### PATCH /pedals/<pedal_id>
- Requires patch:pedals permission (held by Site Owner user)
- Updates data for pedal with id of pedal_id
- Takes JSON with pedal name, pedal type, new price, used price, and manufacturer_id

Ex. 

{'name': 'Pedal X', 'pedal_type': 'Chorus', 'new_price': '$95.00', 'used_price': '$55.00', 'manufacturer_id': 7}

- Returns JSON with updated pedal's id, pedal array, number of pedals, and success value

Example Return

{'updated_pedal': 473, 'pedals': [{"id":1,"manufacturer_id":4,"name":"Soul Vibe SV-74","new_price":"$140.00","pedal_type":"Rotary Speaker Simulator","used_price":"$64.00"}], 'num_pedals': 849, 'success': True}

#### DELETE /manufacturers/<manufacturer_id>
- Requires delete:manufacturers permission (held by Site Owner user)
- Deletes manufacturer with id of manufacturer_id
- Returns JSON with deleted manufacturer's id, manufacturers array, number of manufacturers, and success value

Example Return

{'deleted_manufacturer': 5, 'manufacturers': [{"id":4,"name":"BBE","website_link":"http://www.bbesound.com/"}], 'num_manufacturers': 56, 'success': True}

#### DELETE /pedals/<pedal_id>
- Requires delete:pedals permission (held by Site Owner user)
- Delete pedal with id of pedal_id
- Returns JSON with deleted pedal's id, pedals array, num of pedals, and success value

Example Return

{'deleted_pedal': 352, 'pedals': [{"id":1,"manufacturer_id":4,"name":"Soul Vibe SV-74","new_price":"$140.00","pedal_type":"Rotary Speaker Simulator","used_price":"$64.00"}], 'num_pedals': 848, 'success': True}

## Authentication
Auth is implemented in the auth.py file. It uses the third-party auth service auth0. All relevant variables are included in the auth.py file including auth0 domain, algorithms, and the API audience. There are two roles for accessing features of the API, which include Site Owner and Contributor. The Site Owner role has all permissions. The Contributor has only permissions to access the post endpoints as well as the public get endpoints. Permissions for each endpoint are specified above. 

Note: The setup.sh file contains all the necessary environment variables for authentication. For security reasons it will be deleted from GitHub tracking after successful Udacity review. 
