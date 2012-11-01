# UI Connect

![Screenshot](http://victorneo.github.com/uiconnect/screenshot.png)

UI Connect is a social commerce website built in partial fulfillment for a course project (Software Engineering II).
It is built on top of the Django web framework and several Javascript libraries.

## Features

* Earn reward points when you purchase
* Paypal integration
* Image oriented design built on Bootstrap
* Currency conversion using Money.js
* Image editing with Aviary integration

## Known issues

These issues were not fixed due to the limitation in time (eight academic weeks).
Some technical debt were incurred early in the development and they snowballed towards the end of the development,
providing me a valuable lesson in rapid design and development.

1. Use `SITE_ID` instead of using the first site
2. `django-paypal` should be a git submodule, however the current setup is easier for non-technical users to setup and run
3. Fix the hackish mix of CSS and abuse of `style`
4. URL for Aviary integration should not be hardcoded
5. not fully PEP-8 compliant
