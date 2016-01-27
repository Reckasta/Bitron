'''
This is a reddit bot coded by
/u/Mjone77
/u/honorguard42
maybe some third guy if he decided he wants to
'''
import time
import praw
import random

#this try/except is suppose to surround the whole thing to prevent crash even if some major error occurs that we overlooked
try:
    #log's on to reddit here and set the subreddit
    r = praw.Reddit('who really cares what goes here???')
    #r.login('FacilityAI', '<passwordhere>')
    subreddit = r.get_subreddit('secretsubreddit')
    message = "1" #add replies to this. Make sure to add a ___ (3 underscores) under every message. Hopefully this will allow multiple commands to be called with one comment
    
    #Checks the comments/posts/pm's for commands, and handles them
    def checkForCommands():
        print("checkForCommands")
        
    #Reply to comments
    def commentReply(comment, reply):
        print("commentReply")
        comment.reply(message+"/n[^^See ^^all ^^my ^^commands](wikilinkhere.com)^^|^^other ^^info ^^here")
        #is there a way to do the ^^ effect without having to do it before every word?
        
    #rolls dice and saves each roll in an array, total of the rolls is at the end of the array. This is done so that a table of the rolls can be made if needed.
    def rollDice(amnt, sides):
        total = 0
        rolls = []
        for i in range(0,amnt):
            del i
            roll = random.randrange(sides)+1 
            total+=roll
            rolls.append(roll)
        rolls.append(total)
        return rolls
    
    #makes a cake, probably won't use this actual method in the final code as it's so short
    def cake():
        global message
        message+="Here is your cake sir:\n     ,,,,,\n    _|||||_\n   {~*~*~*~}\n __{*~*~*~*}__\n`-------------`\n___"
        
    #Call everything the bot needs to do here, then write the code above
    while True:
        checkForCommands()
        cake()
        print(message+"done")
        time.sleep(10)
except:
    print('Error')
    time.sleep(30) #we can change the time to whatever