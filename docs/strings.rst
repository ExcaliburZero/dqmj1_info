=======
Strings
=======
Strings are stored in DQMJ1's program binaries and files using a non-standard character encoding.

******************
Character encoding
******************
Each character in a string is 1 byte in length. Strings end with :code:`0xFF` and may have one or more :code:`0x00` after the end for padding purposes. Strings are typically padded out into an integer number of doublewords (32bits / 4 bytes).

Examples
========

First example
-------------

.. code-block::

    37 30 2D 31 29 FF 00 00

Would decode to "slime".

Second example
--------------

:code:`37 30 2D 31 29` being the characters, :code:`FF` denoting the end of the string, and :code:`00 00` being padding to make the string an integer number of doublewords (32bits).

.. code-block::

    1A 36 29 34 0A 01 FF 00 1A 36 29 34 0A 02 FF 00
    1A 33 2D 37 33 32 FF 00 1A 36 29 34 0A 03 FF 00

Would decode into 4 strings:

* "Prep 1"
* "Prep 2"
* "Poison"
* "Prep 3"

*********
Locations
*********
Strings can be stored in different locations depending on the string's puprose.

Strings that are used for core-mechanics (monster species names, interface text, etc.) are typically stored in the ARM9 binary in one of various chunks of strings. These are typically referenced to by another portion of the ARM9 binary in order to organize the strings into tables.

Additional strings (ex. character dialogue) can be stored in other game files (ex. :code:`.evt` files).