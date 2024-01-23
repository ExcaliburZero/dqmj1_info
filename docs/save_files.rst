.. _save_files:

==========
Save Files
==========
Save files are the data that the game uses to keep track of the player and their progress between resets of the game. Save data is stored on the game's cartridge using a custom binary file format.

For details on the exact data layout of the save data binary file format, see `this ImHex pattern file <https://github.com/ExcaliburZero/dqmj1_info/blob/master/pattern_files/dqmj1_save_file.hexpat>`_.

********
Checksum
********
Every save file has a 32bit checksum value which is used by the game to determine if the save file has been corrupted.

When the game loads a save file it recomputes the checksum based on the data stored in the save file and checks if the calculated checksum matches the checksum that is stored in the save file. If the checksum does not match, then the game will show a message indiacting the the game's save file may be corrupted and the game will clear out the save data, forcing the player to start a new game in order to play.

Algorithm
=========
The algorithm for the save data checksum for DQMJ1 is:

Read :code:`10,613` 32bit unisgned integer values starting from index :code:`0x70` in the save file data and sum those integers together, the resulting 32bit unsigned integer is the checksum value.

.. note::

    This value summing algorithm is the same checksum algorithm that is used for DQMJ2, however DQMJ2 starts reading 32bit values from a larger offset in the save data file and also has a separate "header checksum" that applies the same algorithm to the header section of the save data file.

.. todo::

    Add more sections.