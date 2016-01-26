# Bitron
A reddit bot.

# Quic reminder
Reddit bots break all the freaking time, try/except everything please

# Writing
This writes to a log file, will make it easier for me, mjone77, to keep up with errors and junk. Please write whatever you think is super important for me to see to this file. Or maybe we just use to bot to pm ourselves and don't even bother with a log file, either way would work.

# Reply
We'll need a reply class that will handle writing replies to reddit

# Things we need to add
* Give users cake upon request (as requested by /u/Y1ff)

* Admin system - allow specific reddit users access to admin commands through pm
	-Change intro message
	-Add new admins (only super admins can take away admin from users, I guess supers can create new supers too?)
	-turn on/off certain features?
	-other permissions
	
* Intro message
	-replied to new posts made by users not seen before
	-replied to comments asking for it, Command?: !intro
	-This will require an array of all the usernames that have posted to the sub, shouldn't be too hard and can be kept in the .ini file easily

* Roll dice
	-replied to !roll #d#
	-Mjone77 can code this part

* Encrypt/decrypt messages
	-This will be something we add last because it'll take a decent of time and isn't necessary
	-!cipher "message"
	-caesar
	-atbash
	-a1z26
	-vigenere
	
* Some way to take and handle suggestions for new features