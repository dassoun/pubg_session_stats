
## Intro

**PUBG Session Stats** is a script written in Python 2.7

The goal of this script is to get datas from the PUBG APIs, and update files with these datas, so they can be diplayed in Streamlabs OBS, for a given session of gaming (from a start date to the current time).

  

Please note that I discovered Python while writing this script, so feel free to comment the code, and give me some advices.

  

## Configuration

the **conf.py** file has to be completed.

-  **CONST_API_KEY**: PUBG API Devoper Key**, wich can be found here: https://developer.pubg.com/.

-  **CONST_PLAYER_NAME**: the name of the player you want to track.

-  **CONST_LOCAL_TIMEZONE**: the timezone you are in (we can get the timezones here: https://www.php.net/manual/fr/timezones.php).

-  **CONST_PATH**: the path for the data files. The path has to already exist.

## Dependencies

You may have to install some libs to run the script successfully.

I found the libs to install, and the way to do it by searching the errors messages in my favourite serch engine, so don't hesitate to do the same.

  

## Let's make it work !

The goal of this srcipt is to follow the player stats of a gaming session.

So first of all, before beginning our session, we have to set the start date. this can be done with the following command line:

> python.exe UpdatePUBG.py -s

  

This command will set the start date and time, in UTC, in the file **pubg_session_start.txt**.

  

Next, the datas have to be updated.

This can be done with the following command line:

> python.exe UpdatePUBG.py

  

This command has to be executed all along the session in a repeatitive way.

The way I do this, for the moment, is to create a **Windows scheduled task**, with that command line. And this task is repeated every 5 minutes.

This command line can open a console window, so we can change it to:

> pythonw.exe UpdatePUBG.py

  

Finally, the text files have to be linked to text fields in Streamlabs OBS.

The available datas are:

- **Number of games played** (pubg_games.txt)
- **Number of kills** (pubg_kills.txt)
- **Number of wins** (pubg_wins.txt)
- **Number of assists** (pubg_assists.txt)
- **Number of DBNOs** (pubg_dbnos.txt)
- **Kills / Deaths ratio** (pubg_kd.txt)
- **Best rank** (pubg_top.txt)
- **Total damages** (pubg_damage_total.txt)
- **Max damages in a game** (pubg_damage_max.txt)
- **Average damages** (pubg_damage_avg.txt)
