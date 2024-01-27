.. _rng:

========================
Random Number Generation
========================
DQMJ1 uses a random number generator that bases random numbers on the previously generated random number and the count of random numbers that have been generated.

*************
Stored values
*************
The game stores two values in RAM related to RNG:

* :code:`RNG_VALUE` (:code:`0x020BEC9C`) - most recently generated 32bit random number.
* :code:`RNG_COUNTER` (:code:`0x020BEC98`) - count of the number of random numbers that have been generated.

.. todo::

    What value does the counter start at? When does it get reset? Is it kept in the save file and thus consistent between saves?

*********
Algorithm
*********
The following is the algorithm that DQMJ1 uses to generate a new random 32bit number.

.. code:: python

    new_rng_value = rng_value + rng_counter + (rng_value >> 1) + 0x795B3D1F

    rng_counter += 1
    rng_value = new_rng_value