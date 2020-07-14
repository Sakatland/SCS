# Sakat's CoC Script
Python Script to download the data of a clan as well as its members stats (stars and percent done/taken) during a Clan War League (CWL) season in Clash of Clans.

Current Version: 1.6 --- Last update: 2020-07-14

Official thread on the forum of Clash of Clans:

https://forum.supercell.com/showthread.php/1799550-Sakat-s-CoC-Script-Download-your-clan-data-and-CWL-stats?p=12105367

Use this script with our CWL Planning Sheet:

https://forum.supercell.com/showthread.php/1770241-CWL-Planning-Sheet-to-manage-members-in-CWL


# Note
This script is based on ClashOfClansAPI (2.0.6) by Tony Benoy. For more info, please check his github on https://github.com/tonybenoy/cocapi. If you don't have it already please install it with:

	pip3 install cocapi==2.0.6

Get your Token for the API on https://developer.clashofclans.com


# Usage
Enter your Token for the API in Token.txt and run the script.

Due to the limitation of CoC API, some functions only works when a CWL is taking place and before a new clanwar is launched (after the end of a CWL season). But you can still download the data for a previous CWL season with its wartags (each seasons has 28 wartags).

If you want to download the data of a previous season you need to prepare "Warlogs.txt" with the following synthax:

	#29LPJ9JPL
	#29LPJ9CGJ
	...
	#29QR928CP
	#29QR90GVG

You can also use SCS.ipynb in Google Colab or directly opening the following link:

https://colab.research.google.com/drive/13kLQzi4YFqDocNDZypuvMAotJTHqT4vd


# Final word
Check CGLeech.tk, another of my projects!

https://forum.supercell.com/showthread.php/1737664-CGLeech-New-website-to-manage-Clan-Games-activity%21
