=======
bradbot
=======
Discord Bot & Raspberry Pi Hosting Experiment
---------------------------------------------

The goal of this project is to practice building a discord bot in Python, and to host it using the Raspberry Pi Zero W.

Setup
-----
1. Install `poetry <https://python-poetry.org/docs/#installation>`_
2. ``git clone git@github.com:brad90four/bradbot.git``
3. Run ``poetry shell``
4. Run ``poetry install``
5. Run ``pre-commit install``
6. Have a ``.env`` file set up with the variables below:

   - TOKEN
   - SERVER
   - DEV_LOG (channel ID for the on_ready event)

Running the bot locally
-----------------------
1. From the command line, ``cd`` to the ``src`` folder.
2. Run ``py -m bradbot``

Adding ``.gitmessage`` to commit template
-----------------------------------------
1. ``cd`` to the main folder of ``bradbot``
2. ``git config --local commit.template ./.gitmessage``
