"""
                         Sakat's CoC Script v0.8
                         -----------------------

This script is based on ClashOfClansAPI (1.0.4) by Tony Benoy. For more info, please check his github on
                        github.com/tonybenoy/cocapi/
If you don't have it already please install it with "pip3 install cocapi"

Some errors that can happen with the API:
- Error 404: Probably a wrong request URL or an invalid clan tag/location ID/league ID, sometimes it happens if your requests are too fast
- Error 400: You haven't provided all the information required
- Error 429: Too many requests for your keywords
- Error 500: Unknown Error
- Error 503: API is under maintenance
"""


import os, datetime, ast, os.path
from time import sleep
from cocapi import CocApi

# Current version of the Sakat's CoC Script
script_version = "v0.7"

# Clean terminal
os.system("cls")

# Ask to confirm that Token.txt is ready
# If you don't have your token for the API, please create one on developer.clashofclans.com
print("Welcome to Sakat's Coc Script " + script_version + "!\n")
print("For the script to work, you need to enter your Token for the API in a file called 'Token.txt',",)
print("(Token.txt must be located in the same folder as SCS.exe)")
print("Remark: Get your Token on developer.clashofclans.com")
ready_check = input("When Token.txt is ready, press Enter to proceed..\n")

# Check that Token.txt exists in the folder.
while os.path.exists("Token.txt") == False:
    print("Error: Token.txt hasn't been found.")
    print("Please save your Token in a txt file called 'Token.txt' (in the same folder as the script).")
    ready_check = input("When the file is ready, press Enter to proceed..\n")
    os.path.exists("Token.txt")

# Get the API Token and verify Token.txt isn't empty
token = ""
while token == "":
    file_token = open("Token.txt","r", encoding="utf-8")
    token = file_token.read().strip()
    file_token.close()
    if token == "":
        print("Error: Token.txt is empty.")
        print("Please enter your Token for the API in it.")
        ready_check = input("When the file is ready, press Enter to proceed..\n")

# Clear the current screen
print("\n"*100)

# Set a default timeout value for the API (default=10)
timeout = 10
api=CocApi(token,timeout)

# Set the clantag for which the script and check the information from the API
clantag = ("#9PJYL")
print("Default clantag is " + clantag)
check_clantag = input("Do you want to enter another clantag? (y/n) \n")
if (check_clantag.lower() == "y"):
    clantag = input("Enter your clantag (for ex. #9PJYL): ")
    print("The script will check the data for " + clantag)
else:
    print("The script will check the data for " + clantag)
print("\n")

# Get the time value (for various use)
current_time = datetime.datetime.now().strftime("%Y-%m-%d (%HH%M)")

# Maxed number of attempts in case of error when connecting to the API (default=10)
attempt_nb_limit = 10
# Ignore next line
attempt_nb_limit = attempt_nb_limit+1

# Delay in seconds between two requests to the API (default is 0.2)
timer_1 = 0.2

# Clean the current screen
print("\n"*100)

# Ask which data the user want to download
proceed_clan = input("(1/6) Do you want to download the clan and its members data? (y/n) \n")
proceed_warlog = input("(2/6) Do you want to download the warlog of the clan? (y/n) \n")
proceed_currentwar = input("(3/6) Do you want to download the data about current war ? (y/n) \n")
proceed_cwl = input("(4/6) ** Only during a CWL season ** Do you want to download the data about current CWL group? (y/n) \n")
proceed_cwl_details = input("(5/6) Do you want to download the details of individual CWL wars? (y/n) \n")
proceed_cwl_unique = input("(6/6) Do you want to download the details of one single CWL war? (y/n) \n")

# Get the clan and its members data from the API for global usage
print("Downloading the data of the clan and its members for global usage... \n")
sleep(timer_1)
clan_data_1 = api.clan_tag(str(clantag))
attempt_nb = 2
while str(clan_data_1) == "404":
    print("Error 404, trying again in " + str(timer_1) + " seconds...")
    sleep(timer_1)
    print("Attempt #" + str(attempt_nb))
    clan_data_1 = api.clan_tag(str(clantag))
    attempt_nb += 1
    if (attempt_nb == attempt_nb_limit):
        print("Still getting error 404 after " + str(attempt_nb-1) + " attempts, try again later.")
        break
print("\n")

# The following variables are used to store some data of the clan that can be used in the script
# It also checks that the API is not in maintenance
if "reason" in clan_data_1:
    if clan_data_1["reason"] == "inMaintenance":
        print(clan_data_1["message"])
        ready_check = input("Please try again later...")
        quit()
    if clan_data_1["reason"] == "accessDenied.invalidIp":
        print(clan_data_1["message"])
        ready_check = input("Please verify that the IP linked to your API key is correct and restart SCS.exe")
        quit()
else:
    clan_name = clan_data_1["name"]

# Get the clan and members data from the API and saves it in the txt file
if (proceed_clan.lower() == "y"):
    print("Downloading the clan and its members data (1/6)...")
    sleep(timer_1)
    file_1 = open(current_time + " - 01 - Clan Info ["+ clantag + "].txt","w", encoding="utf-8")
    file_1.write(str(clan_data_1["name"]) + " (" + str(clan_data_1["tag"]) + " - lvl " + str(clan_data_1["clanLevel"]) + ")\n\n")
    file_1.write("----------------------------------------\n\n")
    file_1.write('"' + str(clan_data_1["description"]) + '"\n\n')
    file_1.write("----------------------------------------\n\n")
    file_1.write("Location: " + str(clan_data_1["location"]["name"]) + "\n")
    file_1.write("War frequency: " + str(clan_data_1["warFrequency"]) + "\n")
    file_1.write("Required trophies: " + str(clan_data_1["requiredTrophies"]) + "\n")
    file_1.write("Clan points: \n - Home Village = " + str(clan_data_1["clanPoints"]) + "\n - Builder Base = " + str(clan_data_1["clanVersusPoints"]) + "\n")
    file_1.write("Wars won: " + str(clan_data_1["warWins"]) + "\n")
    file_1.write("War ties: " + str(clan_data_1["warTies"]) + "\n")
    file_1.write("Wars lost: " + str(clan_data_1["warLosses"]) + "\n")
    file_1.write("Current war win-streak: " + str(clan_data_1["warWinStreak"]) + "\n\n")
    file_1.write("----------------------------------------\n\n")
    file_1_txt = "Members in details (by trophies order):\n\n"
    member_count = 0
    members_av_lvl = 0
    members_av_troph_hv = 0
    members_av_troph_bh = 0
    members_av_troops_given = 0
    members_av_troops_got = 0
    while (member_count < clan_data_1["members"]):
        # The following sum is used for clan stats average
        members_av_lvl += clan_data_1["memberList"][member_count]["expLevel"]
        members_av_troph_hv += clan_data_1["memberList"][member_count]["trophies"]
        members_av_troph_bh += clan_data_1["memberList"][member_count]["versusTrophies"]
        members_av_troops_given += clan_data_1["memberList"][member_count]["donations"]
        members_av_troops_got += clan_data_1["memberList"][member_count]["donationsReceived"]
        # The data is stored in file_1_txt first so it can be added in the .txt file after clan stats average
        file_1_txt += str(member_count+1) + ") " + str(clan_data_1["memberList"][member_count]["name"]) + " (" + str(clan_data_1["memberList"][member_count]["tag"]) + " - lvl " + str(clan_data_1["memberList"][member_count]["expLevel"]) + ")\n"
        file_1_txt += "Role in the clan: " + str(clan_data_1["memberList"][member_count]["role"]).replace("admin", "elder") + "\n"
        file_1_txt += "Home village: " + str(clan_data_1["memberList"][member_count]["trophies"]) + " trophies (" + str(clan_data_1["memberList"][member_count]["league"]["name"]) + ")\n"
        file_1_txt += "Builder base: " + str(clan_data_1["memberList"][member_count]["versusTrophies"]) + " trophies\n"
        file_1_txt += "Donations:\n- " + str(clan_data_1["memberList"][member_count]["donations"]) + " troops donated\n- " +  str(clan_data_1["memberList"][member_count]["donationsReceived"])  + " troops received\n\n"
        member_count += 1
    file_1.write("Global stats (based on all members):\n")
    file_1.write("Average level: " + str(round(members_av_lvl/clan_data_1["members"], 2)) + "\n")
    file_1.write("Average trophies:\n- Home village = " + str(round(members_av_troph_hv/clan_data_1["members"], 2)) + "\n")
    file_1.write("- Builder base = " + str(round(members_av_troph_bh/clan_data_1["members"], 2)) + "\n")
    file_1.write("Average donation:\n- Troops donated = " + str(round(members_av_troops_given/clan_data_1["members"], 2)) + "\n")
    file_1.write("- Troops received = " + str(round(members_av_troops_got/clan_data_1["members"], 2)) + "\n\n")
    file_1.write("----------------------------------------\n\n")
    file_1.write("The clan has " + str(clan_data_1["members"]) + " members:\n")
    member_count = 0
    members_list = []
    while (member_count < clan_data_1["members"]):
        members_list.append(clan_data_1["memberList"][member_count]["name"])
        member_count += 1
    members_list.sort(key=lambda x: x.lower())
    for member in members_list:
        file_1.write(member + "\n")
    file_1.write("\n----------------------------------------\n\n")
    file_1.write(file_1_txt)
    file_1.write("----------------------------------------\n\n")
    file_1.write("Raw data (as downloaded from the API):\n")
    file_1.write(str(clan_data_1))
    file_1.close()
else:
    print("The download of the clan and its members data has been skipped.")


# Get the warlog data from the API and saves it in the txt file
if (proceed_warlog.lower() == "y"):
    print("Downloading the warlog of the clan (2/6)...")
    sleep(timer_1)
    clan_data_2 = api.clan_war_log(str(clantag))
    # Check that the warlog of the clan is public
    if "reason" in clan_data_2:
        print("Error: " + clan_data_2["reason"])
        print("The warlog of " + clan_name + " is not public, change the clan settings and try again.")
        ready_check = input("Press Enter to continue...\n")
    else:
        file_2 = open(current_time + " - 02 - Warlog ["+ clantag + "].txt","w", encoding="utf-8")
        attempt_nb = 2
        while str(clan_data_2) == "404":
            print("Error 404, trying again in " + str(timer_1) + " seconds...")
            sleep(timer_1)
            print("Attempt #" + str(attempt_nb))
            clan_data_2 = api.clan_war_log(str(clantag))
            attempt_nb += 1
            if (attempt_nb == attempt_nb_limit):
                print("Still getting error 404 after " + str(attempt_nb-1) + " attempts, try again later.")
                break
        file_2.write(str(clan_data_1["name"]) + " (" + str(clan_data_1["tag"]) + " - lvl " + str(clan_data_1["clanLevel"]) + ")\n\n")
        file_2.write("----------------------------------------\n\n")
        file_2_txt = "Warlog in details:\n\n"
        file_2_txt_2 = "Details of last CWL seasons:\n\n"
        warlog_cw_victory = 0
        warlog_av_size = 0
        warlog_av_oppo_lvl = 0
        warlog_av_stars_done = 0
        warlog_av_per_done = 0
        warlog_av_stars_taken = 0
        warlog_av_per_taken = 0
        warlog_av_xp = 0
        warlog_cw_count = 0
        warlog_war_nb = len(clan_data_2["items"])
        # "warlog_war_nb_clean" is used to exclude CWL seasons (which is missing some key in the dictionary)
        warlog_war_nb_clean = warlog_war_nb
        # The following sum is used for clan stats average
        while (warlog_cw_count < warlog_war_nb):
            # The first "if" condition is used to exclude empty data from CWL seasons (parsed separately)
            if (clan_data_2["items"][warlog_cw_count]["opponent"]["clanLevel"]) != 0:
                if clan_data_2["items"][warlog_cw_count]["result"] == "win":
                    warlog_cw_victory +=1
                warlog_av_size += clan_data_2["items"][warlog_cw_count]["teamSize"]
                warlog_av_oppo_lvl += clan_data_2["items"][warlog_cw_count]["opponent"]["clanLevel"]
                warlog_av_stars_done += clan_data_2["items"][warlog_cw_count]["clan"]["stars"]/(clan_data_2["items"][warlog_cw_count]["teamSize"]*3)
                warlog_av_per_done += clan_data_2["items"][warlog_cw_count]["clan"]["destructionPercentage"]
                warlog_av_stars_taken += clan_data_2["items"][warlog_cw_count]["opponent"]["stars"]/(clan_data_2["items"][warlog_cw_count]["teamSize"]*3)
                warlog_av_per_taken += clan_data_2["items"][warlog_cw_count]["opponent"]["destructionPercentage"]
                warlog_av_xp += clan_data_2["items"][warlog_cw_count]["clan"]["expEarned"]
                # The data is stored in file_2_txt first so it can be added in the .txt file after clanwars average
                file_2_txt += "War #" + str(warlog_cw_count+1) + " (ended on " + str(clan_data_2["items"][warlog_cw_count]["endTime"][0:4]) + "-" + str(clan_data_2["items"][warlog_cw_count]["endTime"][4:6]) + "-" + str(clan_data_2["items"][warlog_cw_count]["endTime"][6:8]) + ")\n"
                file_2_txt += str(clan_data_2["items"][warlog_cw_count]["clan"]["name"]) + " was lvl " + str(clan_data_2["items"][warlog_cw_count]["clan"]["clanLevel"]) + " (during that war)\n"
                file_2_txt += "Opponent clan: " + str(clan_data_2["items"][warlog_cw_count]["opponent"]["name"]) + " (" + str(clan_data_2["items"][warlog_cw_count]["opponent"]["tag"]) + " - lvl " + str(clan_data_2["items"][warlog_cw_count]["opponent"]["clanLevel"]) + ")\n"
                file_2_txt += "War size: " + str(clan_data_2["items"][warlog_cw_count]["teamSize"]) + "\n"
                file_2_txt += "War result: " + str(clan_data_2["items"][warlog_cw_count]["result"]) + "\n"
                file_2_txt += "Stars for: " + str(clan_data_2["items"][warlog_cw_count]["clan"]["stars"]) + "/" + str(clan_data_2["items"][warlog_cw_count]["teamSize"]*3) + " with " + str(round(clan_data_2["items"][warlog_cw_count]["clan"]["destructionPercentage"],2)) + "% (done in " + str(clan_data_2["items"][warlog_cw_count]["clan"]["attacks"]) + "/" + str(clan_data_2["items"][warlog_cw_count]["teamSize"]*2) + " attacks)\n"
                file_2_txt += "Stars against: " + str(clan_data_2["items"][warlog_cw_count]["opponent"]["stars"]) + "/" + str(clan_data_2["items"][warlog_cw_count]["teamSize"]*3) + " with " + str(round(clan_data_2["items"][warlog_cw_count]["opponent"]["destructionPercentage"],2)) + "%\n"
                file_2_txt += "XP gained: " + str(clan_data_2["items"][warlog_cw_count]["clan"]["expEarned"]) + "\n\n"
            else:
                file_2_txt_2 += "War season that ended on " + str(clan_data_2["items"][warlog_cw_count]["endTime"][0:4]) + "-" + str(clan_data_2["items"][warlog_cw_count]["endTime"][4:6]) + "-" + str(clan_data_2["items"][warlog_cw_count]["endTime"][6:8]) + "\n"
                file_2_txt_2 += str(clan_data_2["items"][warlog_cw_count]["clan"]["name"]) + " was lvl " + str(clan_data_2["items"][warlog_cw_count]["clan"]["clanLevel"]) + " (during that season)\n"
                # Used to make the value more clear and avoid "None/null" conflit
                if clan_data_2["items"][warlog_cw_count]["result"] == "win":
                    CWL_season_result = "Clan was promoted!"
                elif clan_data_2["items"][warlog_cw_count]["result"] == "tie":
                    CWL_season_result = "Clan was demoted..."
                else:
                    CWL_season_result = "Clan stayed in the same league"
                file_2_txt_2 += "Season result: " + CWL_season_result + "\n"
                file_2_txt_2 += "Stars for: " + str(clan_data_2["items"][warlog_cw_count]["clan"]["stars"]) + "/315 with " + str(round(clan_data_2["items"][warlog_cw_count]["clan"]["destructionPercentage"]*15,0)) + " destruction (done in " + str(clan_data_2["items"][warlog_cw_count]["clan"]["attacks"]) + "/105 attacks)\n"
                file_2_txt_2 += "Stars against: " + str(clan_data_2["items"][warlog_cw_count]["opponent"]["stars"]) + "/315\n\n"
                warlog_war_nb_clean += -1
            warlog_cw_count += 1
        file_2.write("Stats based on the " + str(warlog_war_nb_clean) +" last clanwars:\n")
        file_2.write("Victory: " + str(warlog_cw_victory) + "/" + str(warlog_war_nb_clean) + " (" + str(round(warlog_cw_victory/warlog_war_nb_clean*100, 2)) + "% of victory)\n")
        file_2.write("Average war size: " + str(round(warlog_av_size/warlog_war_nb_clean, 2)) + "\n")
        file_2.write("Average opponent lvl: " + str(round(warlog_av_oppo_lvl/warlog_war_nb_clean, 2)) + "\n")
        file_2.write("Average Stars for: " + str(round(warlog_av_stars_done/warlog_war_nb_clean*100, 2)) + "% (with " + str(round(warlog_av_per_done/warlog_war_nb_clean, 2)) + "% of destruction)\n")
        file_2.write("Average Stars against: " + str(round(warlog_av_stars_taken/warlog_war_nb_clean*100, 2)) + "% (with " + str(round(warlog_av_per_taken/warlog_war_nb_clean, 2)) + "% of destruction)\n")
        file_2.write("Average XP won: " + str(round(warlog_av_xp/warlog_war_nb_clean, 2)) + "\n\n")
        file_2.write("----------------------------------------\n\n")
        file_2.write(file_2_txt)
        file_2.write("----------------------------------------\n\n")
        file_2.write(file_2_txt_2)
        file_2.write("----------------------------------------\n\n")
        file_2.write("Raw data (as downloaded from the API):\n")
        file_2.write(str(clan_data_2))
        file_2.close()
else:
    print("The download of the warlog of the clan has been skipped.")

# Get the information about the current war and saves it in the txt file
if (proceed_currentwar.lower() == "y"):
    print("Downloading the data about current war (3/6)...")
    sleep(timer_1)
    clan_data_3 = api.clan_current_war(str(clantag))
    # Check that the warlog of the clan is public
    if "reason" in clan_data_3:
        print("Error: " + clan_data_3["reason"])
        print("The warlog of " + clan_name + " is not public, change the clan settings and try again.")
        ready_check = input("Press Enter to continue...\n")
    elif clan_data_3["state"] == "notInWar":
        print("Error: " + clan_name + " is currently not warring or engaged in a CWL season, try again once the clan is a normal war.")
        ready_check = input("Press Enter to continue...\n")
    else:
        file_3 = open(current_time + " - 03 - Current War ["+ clantag + "].txt","w", encoding="utf-8")
        attempt_nb = 2
        while str(clan_data_3) == "404":
            print("Error 404, trying again in " + str(timer_1) + " seconds...")
            sleep(timer_1)
            print("Attempt #" + str(attempt_nb))
            clan_data_3 = api.clan_current_war(str(clantag))
            attempt_nb += 1
            if (attempt_nb == attempt_nb_limit):
                print("Still getting error 404 after " + str(attempt_nb-1) + " attempts, try again later.")
                break
        file_3.write(str(clan_data_1["name"]) + " (" + str(clan_data_1["tag"]) + " - lvl " + str(clan_data_1["clanLevel"]) + ")\n\n")
        file_3.write("----------------------------------------\n\n")
        file_3.write("WARNING: SOME OF THESE STATS AREN'T ACCURATE IF THE WAR CURRENTLY TAKING PLACE IS A CWL\n\n")
        file_3.write("Opponent clan: " + str(clan_data_3["opponent"]["name"]) + " (" + str(clan_data_3["opponent"]["tag"]) + " - lvl " + str(clan_data_3["opponent"]["clanLevel"]) + ")\n")
        file_3.write("War size: " + str(clan_data_3["teamSize"]) + "\n")
        file_3.write("War state: " + str(clan_data_3["state"]) + "\n")
        file_3.write("Preparation Time: " + str(clan_data_3["preparationStartTime"][0:4]) + "-" + str(clan_data_3["preparationStartTime"][4:6]) + "-" + str(clan_data_3["preparationStartTime"][6:8]) + "\n")
        file_3.write("Start Time: " + str(clan_data_3["startTime"][0:4]) + "-" + str(clan_data_3["startTime"][4:6]) + "-" + str(clan_data_3["startTime"][6:8]) + "\n")
        file_3.write("End Time: " + str(clan_data_3["endTime"][0:4]) + "-" + str(clan_data_3["endTime"][4:6]) + "-" + str(clan_data_3["endTime"][6:8]) + "\n")
        file_3.write("Stars for: " + str(clan_data_3["clan"]["stars"]) + "/" + str(clan_data_3["teamSize"]*3) + " with " + str(clan_data_3["clan"]["destructionPercentage"]) + "% (done in " + str(clan_data_3["clan"]["attacks"]) + "/" + str(clan_data_3["teamSize"]*2) + " attacks)\n")
        file_3.write("Stars against: " + str(clan_data_3["opponent"]["stars"]) + "/" + str(clan_data_3["teamSize"]*3) + " with " + str(clan_data_3["opponent"]["destructionPercentage"]) + "%\n\n")
        file_3.write("----------------------------------------\n\n")
        file_3_txt = "Individual stats for each members of " + clan_name + ":\n\n"
        cw_member_count = 0
        cw_members_list = []
        while (cw_member_count < clan_data_3["teamSize"]):
            cw_members_list.append(clan_data_3["clan"]["members"][cw_member_count])
            cw_member_count += 1
        cw_members_list = sorted(cw_members_list, key=lambda k: k["mapPosition"])
        cw_member_count = 0
        cw_av_th = 0
        cw_attacks_counter = 0
        cw_av_stars_done = 0
        cw_av_per_done = 0
        cw_defences_counter = 0
        cw_av_stars_taken = 0
        cw_av_per_taken = 0
        while (cw_member_count < clan_data_3["teamSize"]):
            cw_av_th += cw_members_list[cw_member_count]["townhallLevel"]
            # The data is stored in file_3_txt first so it can be added in the .txt file after stats average
            file_3_txt += str(cw_members_list[cw_member_count]["name"]) + " (" + str(cw_members_list[cw_member_count]["tag"]) + " - TH" + str(cw_members_list[cw_member_count]["townhallLevel"]) + ")\n"
            file_3_txt += "War position: " + str(cw_members_list[cw_member_count]["mapPosition"]) + "\n"
            file_3_txt += "Attack(s):\n"
            if "attacks" not in cw_members_list[cw_member_count]:
                file_3_txt += "The player didn't attack yet.\n"
            elif len(cw_members_list[cw_member_count]["attacks"]) == 1:

                cw_attacks_counter += 1
                file_3_txt += "- " + str(cw_members_list[cw_member_count]["attacks"][0]["stars"]) + " stars done with " + str(cw_members_list[cw_member_count]["attacks"][0]["destructionPercentage"]) + "%\n"
            else:
                cw_av_stars_done += cw_members_list[cw_member_count]["attacks"][0]["stars"] + cw_members_list[cw_member_count]["attacks"][1]["stars"]
                cw_av_per_done += cw_members_list[cw_member_count]["attacks"][0]["destructionPercentage"] + cw_members_list[cw_member_count]["attacks"][1]["destructionPercentage"]
                cw_attacks_counter += 2
                file_3_txt += "- " + str(cw_members_list[cw_member_count]["attacks"][0]["stars"]) + " stars done with " + str(cw_members_list[cw_member_count]["attacks"][0]["destructionPercentage"]) + "%\n"
                file_3_txt += "- " + str(cw_members_list[cw_member_count]["attacks"][1]["stars"]) + " stars done with " + str(cw_members_list[cw_member_count]["attacks"][1]["destructionPercentage"]) + "%\n"
            file_3_txt += "Defence(s):\n"
            if cw_members_list[cw_member_count]["opponentAttacks"] == 0:
                file_3_txt += "The player hasn't been attacked yet.\n"
            else:
                cw_av_stars_taken += cw_members_list[cw_member_count]["bestOpponentAttack"]["stars"]
                cw_av_per_taken += cw_members_list[cw_member_count]["bestOpponentAttack"]["destructionPercentage"]
                cw_defences_counter += 1
                file_3_txt += "The player has been attacked " + str(cw_members_list[cw_member_count]["opponentAttacks"]) + " time(s)\n"
                file_3_txt += "Best opponent attack: " + str(cw_members_list[cw_member_count]["bestOpponentAttack"]["stars"]) + " stars done with " + str(cw_members_list[cw_member_count]["bestOpponentAttack"]["destructionPercentage"]) + "%\n"
            file_3_txt += "\n"
            cw_member_count += 1
        file_3.write("Average TH of the clan in the current clanwar: " + str(round(cw_av_th/clan_data_3["teamSize"], 2)) + "\n")
        if clan_data_3["state"] == "preparation":
            file_3.write(clan_name + " is currently in preparation phase, therefore there is no attack/defence stats yet.\n")
            file_3.write("Please run the script again once some players did their attacks.\n\n")
        else:
            file_3.write("In average the members did " + str(round(cw_av_stars_done/cw_attacks_counter, 2)) + " stars and " + str(round(cw_av_per_done/cw_attacks_counter, 2)) + "% (all attacks are counted)\n")
            file_3.write("In average the opponent clan did " + str(round(cw_av_stars_taken/cw_defences_counter, 2)) + " stars and " + str(round(cw_av_per_taken/cw_defences_counter, 2)) + "% (only best attacks are counted)\n\n")
        file_3.write("----------------------------------------\n\n")
        file_3.write(file_3_txt)
        file_3.write("----------------------------------------\n\n")
        file_3.write("Raw data (as downloaded from the API):\n")
        file_3.write(str(clan_data_3))
        file_3.close()
else:
    print("The download of the data about current war has been skipped.")

# Get the information about the current CWL group saves it in the txt file
# This function only works when a CWL is running and before a new CW is started after the end of a season
# The data of a war are only available after its in preparation phase started
# Clan_data_4 = 0 is required for the "if then" added later in the script (when the script automatically write the wartags of the current CWL to Wartags.txt),
# so that, even if the step #4 is skipped (and no CWL is taking place), the step #5 still works (as long as there is a Warlogs.txt in the folder)
clan_data_4 = 0
if (proceed_cwl.lower() == "y"):
    print("Downloading the data about current CWL group (4/6)...")
    sleep(timer_1)
    clan_data_4 = api.clan_leaguegroup(str(clantag))
    attempt_nb = 2
    while str(clan_data_4) == "404":
        print("Error 404, trying again in " + str(timer_1) + " seconds...")
        sleep(timer_1)
        print("Attempt #" + str(attempt_nb))
        clan_data_4 = api.clan_leaguegroup(str(clantag))
        attempt_nb += 1
        if (attempt_nb == attempt_nb_limit):
            print("Still getting error 404 after " + str(attempt_nb-1) + " attempts, try again later.")
            break
    if "reason" in clan_data_4:
        print("\nError: " + clan_name + " is currently not in a CWL season.")
        print("These data are only available when " + clan_name + " is currently taking part to a CWL season.")
        print("Notice that after the end of a season these data stay available until the search for a new clanwar is launched.")
        print("Once a new war is launched after a CWL season, these data aren't available anymore.\n")
        ready_check = input("Press Enter to continue...\n")
    else:
        file_4 = open(current_time + " - 04 - CWL Groups ["+ clantag + "].txt","w", encoding="utf-8")
        file_4.write(str(clan_data_4))
        file_4.close()
else:
    print("The download of the data about current CWL group has been skipped.")

# Get the individual data for each of the 28 CWL wars
# This function only works when a CWL is running or with a Wartags.txt with the 28 war tags already written in it
# Also the data are only available once the preparation phase has started
# Please note that this part of the script will generate four files. The last one is "human friendly"
# while the others are in the format of a dictionary (for advanced uses)
if (proceed_cwl_details.lower() == "y"):

    # Automatically write the wartags of the current CWL to Wartags.txt (only works during a CWL season)
    # The script will only write the wartags that are already available (not equal to "#0")
    # If no CWL season is taking place, the script will skip this step but the user will need to prepare Wartags.txt manually
    if clan_data_4 != 0 and "reason" not in clan_data_4:
        file_war = open("Wartags.txt","w", encoding="utf-8")
        war_round_count = 0
        while (war_round_count < 7):
            war_count = 0
            while (war_count < 4):
                if clan_data_4["rounds"][war_round_count]["warTags"][war_count] != "#0":
                    file_war.write(clan_data_4["rounds"][war_round_count]["warTags"][war_count] + "\n")
                    war_count += 1
                else:
                    war_count = 4
                    war_round_count = 6
            war_round_count += 1
        file_war.close()
    else:
        print("For next step the CWL war tags must be in a text file called Wartags.txt,",)
        ready_check = input("When Wartags.txt is available, press Enter to proceed..\n")

    # Check that Wartags.txt exists in the folder.
    while os.path.exists("Wartags.txt") == False:
        print("Error: warTags.txt hasn't been found.")
        print("Please save the tags of the CWL wars in a txt file called 'Wartags.txt' (in the same folder as the script).")
        ready_check = input("When the file is ready, press Enter to proceed..\n")
        os.path.exists("Wartags.txt")

    # Verify Wartags.txt isn't empty
    # content_5 needs to be declared here to avoid conflict in the loop.
    content_5 = ""
    while content_5 == "":
        file_war = open("Wartags.txt","r", encoding="utf-8")
        content_5 = file_war.read().strip()
        file_war.close()
        if content_5 == "":
            print("Error: Wartags.txt is empty.")
            print("Please enter the tags of the CWL wars in it.")
            ready_check = input("When the file is ready, press Enter to proceed..\n")

    # Get the wartags
    file_5 = open("Wartags.txt","r", encoding="utf-8")
    content_5 = file_5.readlines()
    war_number = len(content_5)
    file_5.close()

    # Prepare the text file
    print("In total there are " + str(war_number) + " wartags available.")
    print("The download of the data will start soon")
    file_6 = open(current_time + " - 05 - CWL Wars ["+ clantag + "].txt","w", encoding="utf-8")
    file_6.write("In total there are " + str(war_number) + " wartags available. \n \n \n")
    file_7 = open(current_time + " - 06 - CWL Wars Dict ["+ clantag + "].txt","w", encoding="utf-8")
    file_7.write("{'cwlWars': [")

    wartag_nb = 1
    for wartag in content_5:
        attempt_nb = 2
        file_6.write("War #" + str(wartag_nb) + " - " + wartag.strip() + ": \n")
        print("Downloading the data for CWL War #" + str(wartag_nb) + " - " + str(wartag.strip()))
        sleep(timer_1)
        wartag = wartag.replace("#", "%23")
        clan_data_5 = api.warleague(str(wartag.strip()))
        while str(clan_data_5) == "404":
            print("Error 404, trying again in " + str(timer_1) + " seconds...")
            sleep(timer_1)
            print("Attempt #" + str(attempt_nb))
            clan_data_5 = api.warleague(str(wartag.strip()))
            attempt_nb += 1
            if (attempt_nb == attempt_nb_limit):
                print("Still getting error 404 after " + str(attempt_nb-1) + " attempts, try again later.")
                break
        wartag_nb += 1
        file_6.write(str(clan_data_5))

        # Check in which wars the clan takes part to indicate it in the .txt file
        war_clan_name = str(clan_data_5["clan"]["name"])
        war_opponent_name = str(clan_data_5["opponent"]["name"])
        if war_clan_name == clan_name or war_opponent_name == clan_name:
            file_6.write("\n")
            file_6.write(clan_name + " is in this war! \n")
        file_6.write("\n \n \n \n")

        # Make a second .txt file with the same data of all cwl wars but in the format of a dictionary
        file_7.write("{'cwTag': '" + wartag.strip() + "', ")
        file_7.write(str(clan_data_5) + ", ")
    file_6.close()

    # The following is used to clean some synthax of the dictionary file (it is very poorly coded)
    file_7.write("_#_END_")
    file_7.close()
    file_7 = open(current_time + " - 06 - CWL Wars Dict ["+ clantag + "].txt","r", encoding="utf-8")
    file_7_cleaner = file_7.read()
    file_7.close()
    file_7_cleaner = file_7_cleaner.replace("Tag': '%23","Tag': '#")
    file_7_cleaner = file_7_cleaner.replace(", {'state'",", 'state'")
    file_7_cleaner = file_7_cleaner.replace("'}, _#_END_","'}]}")
    file_7 = open(current_time + " - 06 - CWL Wars Dict ["+ clantag + "].txt","w", encoding="utf-8")
    file_7.write(file_7_cleaner)
    file_7.close()

    # Due to the limitation of the API, this part of the script isn't able to make the difference between:
    #       A) A player not included in the clanwar
    #       B) A player included in the clanwar BUT who doesn't attack AND isn't attacked (both in the same time)
    # As this situation is very unlikely to happen, it is neglected in the current version of the program.
    data_war_import = open(current_time + " - 06 - CWL Wars Dict ["+ clantag + "].txt","r", encoding="utf-8")
    data_war = data_war_import.read()
    data_war_import.close()
    data_war = ast.literal_eval(data_war)

    # Used to know how many wars are available
    war_total = len(data_war["cwlWars"])

    # Function that outputs the attack & defence stats (stars & percentage) of each members selected for the CWL season
    # "_USED_TO_AVOID_NICKNAME_ERROR_" is used to avoid conflict in the JSON synthax (if a player has "'" in his nickname)
    def cwl_stats_output(clan_opponent):
        member_nb = 0
        dict_members = []
        while member_nb < members_total:
            member_name = data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["name"].replace("'", "_USED_TO_AVOID_NICKNAME_ERROR_")
            member_status = len(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb])
            if member_status == 7:
                dict_members.append("{'Member': '" + member_name + "', 'stars_att': " + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["attacks"][0]["stars"]) + ", 'percent_att': '" + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["attacks"][0]["destructionPercentage"]) + "%', 'stars_def': " + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["bestOpponentAttack"]["stars"]) + ", 'percent_def': '" + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["bestOpponentAttack"]["destructionPercentage"]) + "%'}")
            elif member_status == 6:
                if data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["opponentAttacks"] == 1:
                    dict_members.append("{'Member': '" + member_name + "', 'stars_att': '/', 'percent_att': '/', 'stars_def': " + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["bestOpponentAttack"]["stars"]) + ", 'percent_def': '" + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["bestOpponentAttack"]["destructionPercentage"]) + "%'}")
                else:
                    dict_members.append("{'Member': '" + member_name + "', 'stars_att': " + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["attacks"][0]["stars"]) + ", 'percent_att': '" + str(data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["attacks"][0]["destructionPercentage"]) + "%', 'stars_def': '/', 'percent_def': '/'}")
            else:
                dict_members.append("{'Member': '" + member_name + "', 'stars_att': '/', 'percent_att': '/', 'stars_def': '/', 'percent_def': '/'}")
            member_nb += 1
        file_8.write("{'cwTag': '" + data_war["cwlWars"][war_nb]["cwTag"] + "', 'cwMembers': [" + ", ".join(dict_members))

    # Get the information about the attack & defence stats (stars & percentage) of each members selected for the CWL season
    # It writes two files, one .txt that follow a dictionary synthax and another "human-readable" .txt
    file_8 = open(current_time + " - 07 - CWL Members Stats Dict ["+ clantag + "].txt","w", encoding="utf-8")
    file_8.write("{'cwlStats': [")
    war_nb = 0
    your_opponent_names = []
    your_opponent_tags = []
    your_war_tags = []
    while war_nb < war_total:
        # The match-making randomly decides if a clan is the "host" or the "visitor" of the clanwar
        # This part of the script is used when the clan is considered as the host of the clan war
        if data_war["cwlWars"][war_nb]["clan"]["tag"] == clantag:
            members_total = data_war["cwlWars"][war_nb]["teamSize"]
            your_opponent_names.append(data_war["cwlWars"][war_nb]["opponent"]["name"])
            your_opponent_tags.append(data_war["cwlWars"][war_nb]["opponent"]["tag"])
            your_war_tags.append(data_war["cwlWars"][war_nb]["cwTag"])
            cwl_stats_output("clan")
            file_8.write("]}, ")
        # This part of the script is used when the clan is considered as the visitor of the clan war
        if data_war["cwlWars"][war_nb]["opponent"]["tag"] == clantag:
            members_total = len(data_war["cwlWars"][war_nb]["opponent"]["members"])
            your_opponent_names.append(data_war["cwlWars"][war_nb]["clan"]["name"])
            your_opponent_tags.append(data_war["cwlWars"][war_nb]["clan"]["tag"])
            your_war_tags.append(data_war["cwlWars"][war_nb]["cwTag"])
            cwl_stats_output("opponent")
            file_8.write("]}, ")
        war_nb += 1
    file_8.write("]}")
    file_8.close()

    # The following is used to clean some synthax of the dictionary file (it is very poorly coded)
    file_8 = open(current_time + " - 07 - CWL Members Stats Dict ["+ clantag + "].txt","r", encoding="utf-8")
    file_8_cleaner = file_8.read()
    file_8.close()
    file_8_cleaner = file_8_cleaner.replace("}]}, ]}", "}]}]}")
    file_8 = open(current_time + " - 07 - CWL Members Stats Dict ["+ clantag + "].txt","w", encoding="utf-8")
    file_8.write(file_8_cleaner)
    file_8.close()

    # Group the stats of every members on individual lines to prepare the .txt file to copy-paste in your Google Sheet
    file_8_order = file_8_cleaner.replace("/", "")
    file_8_order = ast.literal_eval(file_8_order)
    file_9 = open(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt","w", encoding="utf-8")
    member_nb = 0
    while member_nb < members_total:
        war_nb = 0
        file_9.write(file_8_order["cwlStats"][war_nb]["cwMembers"][member_nb]["Member"] + "\t")
        while war_nb < war_total/4:
            file_9.write(str(file_8_order["cwlStats"][war_nb]["cwMembers"][member_nb]["stars_att"]) + "\t" + str(file_8_order["cwlStats"][war_nb]["cwMembers"][member_nb]["percent_att"]) + "\t" + str(file_8_order["cwlStats"][war_nb]["cwMembers"][member_nb]["stars_def"]) + "\t" + str(file_8_order["cwlStats"][war_nb]["cwMembers"][member_nb]["percent_def"]) + "\t")
            war_nb += 1
        file_9.write("\n")
        member_nb += 1
    file_9.close()

    # Get ride of "_USED_TO_AVOID_NICKNAME_ERROR_" (used to avoid conflict in the JSON synthax)
    file_9 = open(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt","r", encoding="utf-8")
    file_9_cleaner = file_9.read()
    file_9.close()
    file_9 = open(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt","w", encoding="utf-8")
    file_9.write(file_9_cleaner.replace("_USED_TO_AVOID_NICKNAME_ERROR_", "'"))
    file_9.close()

    # Sort the lines by alphabetic order (based on members name)
    file_9 = open(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt","r", encoding="utf-8")
    file_8_order_final = file_9.readlines()
    file_8_order_final.sort(key=lambda x: x.lower())
    file_9.close()
    # Write the final "human-readable" .txt file
    file_9 = open(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt","w", encoding="utf-8")
    file_9.write("Names of opponent clans:\n")
    file_9.write("\n".join(your_opponent_names) + "\n\n\n")
    file_9.write("Tags of opponent clans:\n")
    file_9.write("\n".join(your_opponent_tags) + "\n\n\n")
    file_9.write("Wartags available for the war to which " + clan_name + " takes part to:\n")
    file_9.write("\n".join(your_war_tags) + "\n\n\n")
    file_9.write("Individual stats of the participating members through the available CWL wars:\n")
    for item in file_8_order_final:
        file_9.write(item)
    file_9.close()
    print(("\n \n"))
else:
    print("The download of the details of individual CWL wars has been skipped.")

# Get the information about one particular CWL
if (proceed_cwl_unique.lower() == "y"):
    wartag_individual = input("Please enter the tag of the CWL war you want to download the details about (for ex: #ABCDEFGH): ")
    print("Downloading the data for CWL War " + str(wartag_individual.strip()))
    file_10 = open(current_time + " - 09 - Individual CWL War ["+ clantag + "].txt","w", encoding="utf-8")
    file_10.write("Details for war " + wartag_individual.strip() + ": \n")
    sleep(timer_1)
    attempt_nb = 2
    wartag_individual = wartag_individual.replace("#", "%23")
    clan_data_9 = api.warleague(str(wartag_individual.strip()))
    while str(clan_data_9) == "404":
        print("Error 404, trying again in " + str(timer_1) + " seconds...")
        sleep(timer_1)
        print("Attempt #" + str(attempt_nb))
        clan_data_9 = api.warleague(str(wartag_individual.strip()))
        attempt_nb += 1
        if (attempt_nb == attempt_nb_limit):
            print("Still getting error 404 after " + str(attempt_nb-1) + " attempts, try again later.")
            break
    file_10.write(str(clan_data_9))
    file_10.close()
    print(("\n \n"))
else:
    print("The download of the details of one single CWL war has been skipped.")

# Confirmation message
print("\n")
print("Download finished (100%)")
print("Raw data successfully written in:")
if (proceed_clan.lower() == "y"):
    print(current_time + " - 01 - Clan Info ["+ clantag + "].txt")
if (proceed_warlog.lower() == "y") and "reason" not in clan_data_2:
    print(current_time + " - 02 - Warlog ["+ clantag + "].txt")
if (proceed_currentwar.lower() == "y") and (("reason" not in clan_data_3) and (clan_data_3["state"] != "notInWar")):
    print(current_time + " - 03 - Current War ["+ clantag + "].txt")
if os.path.exists(current_time + " - 04 - CWL Groups ["+ clantag + "].txt") == True:
        print(current_time + " - 04 - CWL Groups ["+ clantag + "].txt")
if (proceed_cwl_details.lower() == "y"):
    print(current_time + " - 05 - CWL Wars ["+ clantag + "].txt")
    print(current_time + " - 06 - CWL Wars Dict ["+ clantag + "].txt")
    print(current_time + " - 07 - CWL Members Stats Dict ["+ clantag
    + "].txt")
    print(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt")
if (proceed_cwl_unique.lower() == "y"):
    print(current_time + " - 09 - Individual CWL War ["+ clantag + "].txt")
if (proceed_clan.lower() != "y") and ((proceed_warlog.lower() != "y") or "reason" in clan_data_2) and ((proceed_currentwar.lower() != "y") or "reason" in clan_data_3 or clan_data_3["state"] == "notInWar") and  (os.path.exists(current_time + " - 04 - CWL Groups ["+ clantag + "].txt") != True) and (proceed_cwl_details.lower() != "y") and (proceed_cwl_unique.lower() != "y"):
    print("No file has been written.")
print("\n")
print("Sakat's CoC Script " + script_version + " - Clan Valais (#9PJYL)")
print("     Discover another project by us on:")
print("     =======>  www.cgleech.tk <=======\n")
finish = input("Press Any Key to quit.\n")
