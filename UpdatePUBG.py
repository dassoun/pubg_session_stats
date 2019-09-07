import requests
import json
import datetime as DT
import pytz
import sys
import conf
import argparse
import os

# Update file
def update_source_file(file_path, value):
    file = open(file_path, "w")
    file.write(value)
    file.close
    return

#   Init data files
def init_data_files():
    update_source_file(file_games, "0")
    update_source_file(file_kills, "-")
    update_source_file(file_wins, "-")
    update_source_file(file_assists, "-")
    update_source_file(file_dbno, "-")
    update_source_file(file_kd, "-")
    update_source_file(file_kda, "-")
    update_source_file(file_top, "-")
    update_source_file(file_avg_rank, "-")
    update_source_file(file_total_damages, "-")
    update_source_file(file_max_damages, "-")
    update_source_file(file_avg_damages, "-")

    return

# The destination directory has to exist
if not os.path.isdir(conf.CONST_PATH):
    print("Path {} not found.".format(conf.CONST_PATH))
    sys.exit(1)

# Setting the different files path
file_session_start = conf.CONST_PATH + "\\" + conf.CONST_FILE_SESSION_START
file_games = conf.CONST_PATH + "\\" + conf.CONST_FILE_GAMES
file_kills = conf.CONST_PATH + "\\" + conf.CONST_FILE_KILLS
file_wins = conf.CONST_PATH + "\\" + conf.CONST_FILE_WIN
file_assists = conf.CONST_PATH + "\\" + conf.CONST_FILE_ASSIST
file_dbno = conf.CONST_PATH + "\\" + conf.CONST_FILE_DBNO
file_kd = conf.CONST_PATH + "\\" + conf.CONST_FILE_KD
file_kda = conf.CONST_PATH + "\\" + conf.CONST_FILE_KDA
file_top = conf.CONST_PATH + "\\" + conf.CONST_FILE_TOP
file_avg_rank = conf.CONST_PATH + "\\" + conf.CONST_FILE_AVG_RANK
file_total_damages = conf.CONST_PATH + "\\" + conf.CONST_FILE_TOTAL_DAMAGE
file_max_damages = conf.CONST_PATH + "\\" + conf.CONST_FILE_DAMAGE
file_avg_damages = conf.CONST_PATH + "\\" + conf.CONST_FILE_AVG_DAMAGE

# Set the local datetime in UTC
local_tz = pytz.timezone (conf.CONST_LOCAL_TIMEZONE)
dt_now_without_tz = DT.datetime.now()
dt_now_with_tz = local_tz.localize(dt_now_without_tz, is_dst=None) # No daylight saving time
dt_now_in_utc = dt_now_with_tz.astimezone(pytz.utc)

# Let's parse the command line
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--session_start", help="set the datetime of the beginning of the session, and reinit the data files",
                    action="store_true")
args = parser.parse_args()

if args.session_start:
    print("Session start")

    update_source_file(file_session_start, dt_now_in_utc.strftime('%Y-%m-%d %H:%M:%S %Z'))
    update_source_file(file_games, "0")
    update_source_file(file_kills, "-")
    update_source_file(file_wins, "-")
    update_source_file(file_assists, "-")
    update_source_file(file_dbno, "-")
    update_source_file(file_kd, "-")
    update_source_file(file_top, "-")
    update_source_file(file_total_damages, "-")
    update_source_file(file_max_damages, "-")
    update_source_file(file_avg_damages, "-")
    sys.exit()

# if CONST_FILE_SESSION_START does not exist, we have to initialize the session
if not os.path.exists(file_session_start):
    print("file {} not found.".format(file_session_start))
    print("please execute the command")
    print("python UpdatePUBG_api.py -s")
    print("to initialize your session.")
    sys.exit(1)
else:
    with open(file_session_start) as file:
        dt_session_start = DT.datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S %Z")

# Variables initialization
nb_match        = 0             # Number of played matchs
nb_kill         = 0             # Number of kills
nb_win          = 0             # Number of Top 1
nb_assist       = 0             # Number of assists
nb_dbno         = 0             # Number of DBNOs
nb_death        = 0             # Number of deaths
win_place       = 100           # Best rank
total_damage    = 0             # Total damages
max_damage      = 0             # Max damages in a game
avg_damage      = 0             # average damages
top_repeat      = 0             # How many times the player complete his best rank

# Set the header for PUBG API calls
headers = {
    "Authorization": "Bearer " + conf.CONST_API_KEY,
    "Accept": "application/vnd.api+json"
}

# Get the list of the matchs for the player
player_stats_url = conf.CONST_URL + "/" + conf.CONST_PLATFORM_STEAM + "/" + "players?filter[playerNames]=" + conf.CONST_PLAYER_NAME

r = requests.get(player_stats_url, headers = headers)
if r.status_code == 200:
    print("Successfully Connected!!!")
else:
    print("Failed to Connect!!!")
    sys.exit(1)

player_stat = json.loads(r.text)

# print(json.dumps(player_stat, sort_keys=False, indent=4))

# We extract the match id list from the player object
match_id_list = player_stat["data"][0]["relationships"]["matches"]["data"]

for match in match_id_list:
    match_id = match["id"]
    match_url = conf.CONST_URL + "/" + conf.CONST_PLATFORM_STEAM + "/" + "matches/{}".format(match_id)
    match_r = requests.get(match_url, headers = headers)
    if match_r.status_code != 200:
        print("Failed to Connect!!!")
    match_stat = json.loads(match_r.text)

    # Get the creation date of the match datas
    created_at = match_stat["data"]["attributes"]["createdAt"]
    
    dt_created_at = DT.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")

    if dt_created_at >= dt_session_start:
        nb_match += 1

        included_list = match_stat["included"]
        # print(json.dumps(included_list, sort_keys=False, indent=4))

        for included in included_list:
            if (included["type"] == "participant" and included["attributes"]["stats"]["name"] == conf.CONST_PLAYER_NAME):
                # print(json.dumps(included, sort_keys=False, indent=4))
                nb_kill += included["attributes"]["stats"]["kills"]
                if included["attributes"]["stats"]["winPlace"] == 1:
                    nb_win += 1
                else:
                    nb_death += 1
                nb_assist += included["attributes"]["stats"]["assists"]
                try:
                    nb_dbno += included["attributes"]["stats"]["DBNOs"]
                except KeyError:
                    nb_dbno += 0
                if included["attributes"]["stats"]["winPlace"] < win_place:
                    win_place = included["attributes"]["stats"]["winPlace"]
                    top_repeat = 1
                elif included["attributes"]["stats"]["winPlace"] == win_place:
                    top_repeat += 1
                total_damage += included["attributes"]["stats"]["damageDealt"]
                if included["attributes"]["stats"]["damageDealt"] > max_damage:
                    max_damage = round(included["attributes"]["stats"]["damageDealt"])

if nb_match == 0:
    init_data_files()

    print("nb games = 0")
    print("nb kill = -")
    print("nb win = -")
    print("nb assist = -")
    print("nb dbno = -")
    print("win place = -")
    print("total damages = -")
    print("avg damages = -")
    print("max damages = -")
else:
    update_source_file(file_games, str(nb_match))
    update_source_file(file_kills, str(nb_kill))
    update_source_file(file_wins, str(nb_win))
    update_source_file(file_assists, str(nb_assist))
    update_source_file(file_dbno, str(nb_dbno))
    if nb_death > 0:
        update_source_file(file_kd, str(round(float(nb_kill) / float(nb_death), 2)))
        update_source_file(file_kda, str(round(float(nb_kill + nb_assist) / float(nb_death), 2)))
    else:
        update_source_file(file_kd, str(nb_kill))
        update_source_file(file_kd, str(nb_kill + nb_assist))
    # If the top rank occured more than once, we show it
    str_win_place = str(win_place)
    if win_place > 1 and top_repeat > 1:
        str_win_place += " (x{})".format(top_repeat)
    update_source_file(file_top, str_win_place)
    update_source_file(file_avg_rank, str(round(float(rank_sum) / float(nb_match), 2)))
    update_source_file(file_total_damages, str(round(total_damage)))
    if nb_match > 0:
        avg_damage = str(round(float(total_damage) / float(nb_match), 2))
    else:
        avg_damage = 0
    update_source_file(file_avg_damages, str(round(float(avg_damage), 2)))
    update_source_file(file_max_damages, str(round(float(max_damage), 2)))

    print("nb games = {}".format(nb_match))
    print("nb kill = {}".format(nb_kill))
    print("nb win = {}".format(nb_win))
    print("nb assist = {}".format(nb_assist))
    print("nb dbno = {}".format(nb_dbno))
    print("win place = {}".format(str_win_place))
    print("total damages = {}".format(total_damage))
    print("avg damages = {}".format(avg_damage))
    print("max damages = {}".format(max_damage))
