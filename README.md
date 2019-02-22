# Sakat's CoC Script
Python Script to download the data of a clan as well as its members stats (stars and percent done/taken) during a Clan War League (CWL) season in Clash of Clans.

Last update: 2019-02-21
Current Version: 0.4


# Note
This script is based on ClashOfClansAPI (1.0.4) by Tony Benoy. For more info, please check his github on https://github.com/tonybenoy/cocapi. If you don't have it already please install it with:

	pip3 install cocapi

Get your Token for the API on https://developer.clashofclans.com


# Usage
Due to the limitation of CoC API, some functions only works when a CWL is taking place and before a new clanwar is launched (after the end of a CWL season). But you can still download the data for a previous CWL season with its wartags (each seasons has 28 wartags).

If you want to download the data of a previous season you need to prepare "Warlogs.txt" with the following synthax:

	#29LPJ9JPL
	#29LPJ9CGJ
	...
	#29QR928CP
	#29QR90GVG
