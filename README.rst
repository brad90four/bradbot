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

Running the bot locally
-----------------------
1. From the command line, ``cd`` to the ``src`` folder.
2. Run ``py -m bradbot``

Adding ``.gitmessage`` to commit template
-----------------------------------------
1. ``cd`` to the main folder of ``bradbot``
2. ``git config --local commit.template ./.gitmessage``

Fun with the Strava API
-----------------------
.. image::  https://github.com/brad90four/bradbot/blob/main/src/exts/strava_vis_6463534976.gif

Steps to work with the stand alone `strava.py`
====================================================
1. Create a Strava Application

    -  You will need your Client ID and Client Secret

2. Copy the url

   ``http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,activity:read_all``

   into your browser and place your Client ID in the placeholder.
3. Approve the application on the prompt and wait for the redirect url to appear.
4. When the redirect url is shown in your browser, copy the Authorization Code shown in it.

   ``localhost/exchange_token?stat=&code=`` **12345verylongcodehere12345** ``&scope=read,activity:read_all,read_all``

5. Run the ``curl`` request with your Client ID, Client Secret and the Authorization Code from above in your terminal.

   ``curl -X POST https://www.strava.com/oauth/token -F client_id=YOURCLIENTID -F client_secret=YOURCLIENTSECRET -F code=AUTHORIZATIONCODE -F grant_type=authorization_code``

6. Use the ``access_token`` provided in the response as the ``.env`` variable ``STRAVA_TOKEN``.

7. From the command line, run ``python strava.py`` from the ``\bradbot\src\exts\`` directory.
