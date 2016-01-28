# Bitron
A reddit bot.

# Quick reminder
Reddit bots break all the freaking time, try/except everything please

# How to bot speaks
I (/u/mjone77) don't know the lore of the sub all that well, so I'm not sure how the bot should say things. Feel free to change his comment replies to better match the lore of the sub.

# Reply
We'll need a reply class that will handle writing replies to reddit

# Things we need to add
* Give users cake upon request (as requested by /u/Y1ff)
	
	-this will be taken care under verbage. the regexes I have are robust-ish

* Admin system  
 	-allow specific reddit users access to admin commands through pm  
	-Change intro message  
	-Add new admins (only super admins can take away admin from users, I guess supers can create new supers too?)  
	-turn on/off certain features?  
	-other permissions

	What exactly is the admin system trying to do? Right now, we use auto mod for the admin kind of stuff, that can change,but I was just wondering.
	
* Intro message  
 	-replied to new posts made by users not seen before  
	-replied to comments asking for it, Command?: !intro 
		
		~ehhhhhhhh, my mentality when I was designing it was for it to be natural that's why I have a response to 'where am I'. but If we have the usernames stored then this seems correct.
	-This will require an array of all the usernames that have posted to the sub, shouldn't be too hard and can be kept in the .ini file easily
		
		~I like this, I didn't think of it and It seems like a legit solution

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

	these are the fun bits, thats what the bot is about imo
	
* Some way to take and handle suggestions for new features
