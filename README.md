PyTado -- Pythonize your central heating
========================================

Author: Chris Jewell <chrism0dwk@gmail.com>

Licence: GPL v3

Copyright: Chris Jewell 2016

PyTado is a Python module implementing an interface to the Tado web API.  It allows a user to interact with their Tado heating system for the purposes of monitoring or controlling their heating system, beyond what Tado themselves currently offer.

It is hoped that this module might be used by those who wish to tweak their Tado systems, and further optimise their heating setups.

Disclaimer
----------
Besides owning a Tado system, I have no connection with the Tado company themselves.  PyTado was created for my own use, and for others who may wish to experiment with personal Internet of Things systems.  I receive no help (financial or otherwise) from Tado, and have no business interest with them.  This software is provided without warranty, according to the GNU Public Licence version 3, and should therefore not be used where it may endanger life, financial stakes, or cause discomfort and inconvenience to others.

Example basic usage
-------------------

    >>> from PyTado import Tado
    >>> t = Tado('my@username.com', 'mypassword')
    >>> climate = t.getClimate(zone=1)

Development
-----------
This software is at a purely experimental stage.  If you're interested and can write Python, clone the Github repo, drop me a line, and get involved!


Best wishes and a warm winter to all!

Chris Jewell