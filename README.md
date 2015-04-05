# HRCSLA V2
An app to log the reports of an HRC channel for a Minecraft network

This is the source code for the Hacker Report Chat Slack Logging App (HRCSLA). 
It uses the python and the slacker module to process chat history and log results in a remote database.
The HRCSLA is intended to run parallel with a database processing webapp to display the reports.

Features:

Updates and processes reports every 60 seconds.
Connects to a remote database to send the (processed) reports to.
Stores data locally in case of error with said database.
Allows adding/removing reports manually in case of mistakes or errors easily.
User verification such that general users are not restricted nor can upset the system.
Custom ban/clean verdict options to allow for other languages as well as potentially logging non-hacker reports.
This system is not restricted to a Minecraft network, but is configured for a video game server in which players report cheaters!

For questions and inquiries concerning the HRCSLA, contact Matt (in game: ma56nin) at ma56nin@hotmail.com or my GitHub e-mail.
