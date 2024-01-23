.. _monsters:

========
Monsters
========
Individual monsters have various information describing them.

****
Name
****
Each monster has a name, given by the player. The name is encoded as a :ref:`string <strings>`. The name can have up to 8 characters.

*******
Species
*******
Each monster has a 16bit unsigned integer noting its species (ex. Slime, Dracky, etc.).

****
Rank
****
Each monster has a 8bit unsigned integer noting its rank (ex. F, E, D, C, etc.). Note that while monster species each have an associated rank, the rank for each individual monster is stored separate from the species id and thus could be incosistent with the monster species' rank if edited.

* 1=F
* 2=E
* 3=D
* 4=C
* 5=B
* 6=A
* 7=S
* 8=X
* 9=???

.. todo::

    Add remaining sections.