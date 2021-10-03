Your Game Title
===============

Entry in PyWeek #12  <http://www.pyweek.org/12/>
URL: http://pyweek.org/e/petraszd-pw-12/
Team: Petras Zdanavicius
Members: petraszd
License: see LICENSE.txt


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run::

  python run_game.py


Libraries required:

- pyglet
- cocos2d


How to Play the Game
--------------------

- Click onto squares to split them into 9 squares.
- Hold and drag squares to shoot them at targets.
- You must destroy all circles to win the game.


Development notes
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

