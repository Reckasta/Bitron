"""
This is totally a bot I made
If you steal it... That's Ok I don't mind
better for small subreddits
Wow I'm actually amazed this works?
"""
#Imports
import praw
import re
import time
import random
#Parser
def parseComment(comment):
	result = ""
	comment = str(comment)
	print(comment)
	randomNumber = random.randrange(0, 100, 1)
	decimal = random.randrange(0, 99, 1)

	#chance
	match = re.search('\s*AI what (are my chances|is the probability)',comment,re.IGNORECASE)
	if match:
		result += str(randomNumber)+'.'+str(decimal)+'%\n\n'
		if randomNumber < 20:
			result += 'If I could laugh, I would be lauging at you\n\n*Dispensing popcorn*\n\n'
		elif randomNumber < 40:
			result += 'This will be fun to watch\n\n'
		elif randomNumber < 60:
			result += 'You are better off flipping a coin\n\n'
		elif randomNumber < 80:
			result += 'You now are considered to have an average human success rate\n\n'
		else:
			result += 'How could you possibly fail... Probably hilariously\n\n'
	
	#dispense
	match = re.search('(\s*AI (dispense|make it rain)\s)(\S+)',comment,re.IGNORECASE)
	if match:
		if randomNumber <= 10:
			result = 'No\n\n'
		else:
			result += '*Dispensing '+match.group(3)+'*\n\n'

	#verbing
	match = re.search('(\s*AI (can you|please)\s)(\S+)',comment,re.IGNORECASE)
	if match:
		randomNumber = random.randrange(0, 100, 1)
		if randomNumber <= 10:
			result = 'No\n\n'
		else:
			result += '*'+match.group(3)+'-ing*\n\n'

	#self destruct
	match = re.search('\s*AI\s(self(\x2D|\s)?destruct|kill me|suicide)',comment,re.IGNORECASE)
	if match:
		result += 'OK, you will explode in 3'+'\n\n'
		result += '2\n\n'
		result += '1\n\n'
		result += '*Drops a live grenade at your feet*\n\n'

	#nonsense
	match = re.search("(\s*yo)?u('re)?(/sa)? monster",comment,re.IGNORECASE)
	if match:
		result += "A monster? Hah! That's a funny joke. Especially with *your* record."+'\n\n'

	#end of all results
	if result != "":
		result += '[List of AI Commands](http://secretsubreddit.wikia.com/wiki/AI_Commands)'
	return result

# log in and initialization
agent = 'Facility AI by /u/honorguard42'

already_done = []

ui = input("Safe mode(y/n)? ")
if ui == 'y':
	safe = True
else:
	safe = False

backup = open('commentId.txt','r+')

for lines in backup:
	already_done.append(lines)
backup.close()
#Scans for comments
while True:
	#If error try again in 10 seconds
	try:
		r = praw.Reddit(user_agent=agent)
		r.login('FacilityAI', '<passwordhere>')
		recentComments = r.get_comments('secretSubreddit')
		#Finished comment list
		backup = open('commentId.txt','r+')
		for comment in recentComments:
			reply = ""
			#make sure this is a string, having issues with this
			commentId = str(comment.id)+'\n'
			if commentId not in already_done:
				reply = parseComment(comment)
				already_done.append(commentId)
				backup.write(commentId)
			if reply != "":
				if not safe:
					comment.reply(reply)
					print(reply)
		safe = False
		backup.close()
		time.sleep(30)
	except:
		time.sleep(10)