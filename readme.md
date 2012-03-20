About
=====

This app is a collection of "stuff" that I end up using on every django project. I'll be moving things into here as I run into them.

Installation
============

The easy way to install is to use pip:

    pip install django-support

then just add support to INSTALLED_APPS in settings.py:

    INSTALLED_APPS = (
    	#...
        'support',
    )

and context processors:
    
    TEMPLATE_CONTEXT_PROCESSORS = (
        #...
        'support.context_processors.app_name',
    )


Boom.

Settings
========

Page Title
----------

The page title is built using the `APP_NAME` variable from settings plus whatever you send to the template as `page_title`.

This will be rendered in the following way:

    App Name | page_title

Validators
==========

`validate_unique_email` and `validate_unique_username` are available for use. Both of these assume that you are using the django
provided `User` model and that you force both e-mails and usernames to be lower case.

Forms
=====

Location
--------

if using the form location field you need to set `GET_CREATE_LOCATION_FUNCTION` in your settings.py.

This is a string path to a location function. This function should take a latitude and longitude and return a location object.

something like:

    def get_location(lat, lng):
        # get your location object here
        
        return location_object

