'''
This is a reddit bot coded by
/u/Mjone77
/u/honorguard42
maybe some third guy if he decided he wants to
'''
import time
import praw

#this try/except is suppose to surround the whole thing to prevent crash even if some major error occurs that we overlooked
try:
    #log's on to reddit here and set the subreddit
    r = praw.Reddit('who really cares what goes here???')
    r.login('FacilityAI', '<passwordhere>')
    subreddit = r.get_subreddit('secretsubreddit')
    message = "" #add replies to this. Make sure to add a ___ (3 underscores) under every message. Hopefully this will allow multiple commands to be called with one comment
    
    #Checks the comments/posts/pm's for commands, and handles them
    def checkForCommands():
        print("checkForCommands")
        
    #Reply to comments
    def commentReply(comment, reply):
        print("commentReply")
        comment.reply(message+"/n[^^See ^^all ^^my ^^commands](wikilinkhere.com)^^|^^other ^^info ^^here")
        #is there a way to do the ^^ effect without having to do it before every word?
    
    #Call everything the bot needs to do here, then write the code above
    while True:
        checkForCommands()
except:
    time.sleep(60) #we can change the time to whatever