"""
                         Sakat's CoC Script v0.6
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
script_version = "v0.6"

# Clean terminal
os.system("cls")

# Ask to confirm that Token.txt is ready
# If you don't have your token for the API, please create one on developer.clashofclans.com
print("Welcome in Sakat's Coc Script " + script_version + "!\n")
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
    file_1.write(str(clan_data_1))
    file_1.close()
else:
    print("The download of the clan and its members data has been skipped.")

# Get the warlog data from the API and saves it in the txt file
if (proceed_warlog.lower() == "y"):
    print("Downloading the warlog of the clan (2/6)...")
    sleep(timer_1)
    file_2 = open(current_time + " - 02 - Warlog ["+ clantag + "].txt","w", encoding="utf-8")
    clan_data_2 = api.clan_war_log(str(clantag))
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
    file_2.write(str(clan_data_2))
    file_2.close()
else:
    print("The download of the warlog of the clan has been skipped.")

# Get the information about the current war and saves it in the txt file
if (proceed_currentwar.lower() == "y"):
    print("Downloading the data about current war (3/6)...")
    sleep(timer_1)
    file_3 = open(current_time + " - 03 - Current War ["+ clantag + "].txt","w", encoding="utf-8")
    clan_data_3 = api.clan_current_war(str(clantag))
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
    if clan_data_4["reason"] == "notFound":
        print("\nError: " + clan_name + " is currently not in a CWL season.")
        print("These data are only available when " + clan_name + " is currently taking part to a CWL season.")
        print("Notice that after the end of a season these data stay available until the search for a new clanwar is launched.")
        print("Once a new war is launched after a CWL season it is gone.\n")
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
    # The script will only write the wartags that are already available (not equal to "#000000000")
    # If no CWL season is taking place, the script will skip this step but the user will need to prepare Wartags.txt manually
    if clan_data_4 != 0 and clan_data_4["reason"] != "notFound":
        file_war = open("Wartags.txt","w", encoding="utf-8")
        war_round_count = 0
        while (war_round_count < 7):
            war_count = 0
            while (war_count < 4):
                if clan_data_4["rounds"][war_round_count]["warTags"][war_count] != "#000000000":
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
    def cwl_stats_output(clan_opponent):
        member_nb = 0
        dict_members = []
        while member_nb < members_total:
            member_name = data_war["cwlWars"][war_nb][clan_opponent]["members"][member_nb]["name"]
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
if (proceed_warlog.lower() == "y"):
    print(current_time + " - 02 - Warlog ["+ clantag + "].txt")
if (proceed_currentwar.lower() == "y"):
    print(current_time + " - 03 - Current War ["+ clantag + "].txt")
if os.path.exists(current_time + " - 04 - CWL Groups ["+ clantag + "].txt") == True:
        print(current_time + " - 04 - CWL Groups ["+ clantag + "].txt")
if (proceed_cwl_details.lower() == "y"):
    print(current_time + " - 05 - CWL Wars ["+ clantag + "].txt")
    print(current_time + " - 06 - CWL Wars Dict ["+ clantag + "].txt")
    print(current_time + " - 07 - CWL Members Stats Dict ["+ clantag + "].txt")
    print(current_time + " - 08 - CWL Members Stats ["+ clantag + "].txt")
if (proceed_cwl_unique.lower() == "y"):
    print(current_time + " - 09 - Individual CWL War ["+ clantag + "].txt")
if (proceed_clan.lower() != "y") and (proceed_warlog.lower() != "y") and (proceed_currentwar.lower() != "y") and  (os.path.exists(current_time + " - 04 - CWL Groups ["+ clantag + "].txt") != True) and (proceed_cwl_details.lower() != "y") and (proceed_cwl_unique.lower() != "y"):
    print("No file has been written.")
print("\n")
print("Sakat's CoC Script " + script_version + " - Clan Valais (#9PJYL)")
print("     Discover another project by us on:")
print("     =======>  www.cgleech.tk <=======\n")
finish = input("Press Enter to quit.\n")
