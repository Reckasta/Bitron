'''
This is a reddit bot coded by
/u/Mjone77
/u/honorguard42
maybe some third guy if he decided he wants to
'''
import time
import praw
import random
import sys
import configparser

#this try/except is suppose to surround the whole thing to prevent crash even if some major error occurs that we overlooked
try:
    #This sets up the variables and junk from the ini file, also creates an ini file if it is missing
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        welcomeMessage = config['Welcome']['message']
        refreshMessage = config['Welcome']['refresh']
        alreadyWelcomed = config['Welcome']['alreadyWelcomed'].split()
        admins = config['Admin']['users'].split(',')
    except:
        config = configparser.ConfigParser()
        config['Welcome'] = {'message': 'Welcome!',
                             'alreadyWelcomed': '',
                             'refresh': 'Refresh'}
        config['Admin'] = {'users': ''}
        with open('config.ini','w') as configfile:
            config.write(configfile)
        print("Please complete generated config.ini")
        sys.exit()
    
    '''
    #log's on to reddit here and set the subreddit
    r = praw.Reddit('who really cares what goes here???')
    #r.login('FacilityAI', '<passwordhere>')
    subreddit = r.get_subreddit('secretsubreddit')
    '''
    message = "" #add replies to this. Make sure to add a \n___\n (3 underscores) after every message. Hopefully this will allow multiple commands to be called with one comment
    
    #Checks the comments/posts/pm's for commands, and handles them
    def checkForCommands():
        print("checkForCommands")
        
    #Reply to comments
    def commentReply(): #Don't forget takes in comment
        global message
        print("commentReply")
        print(message+"^^[meta][^^See ^^all ^^my ^^commands](wikilinkhere.com)^^|[suggest ^^new ^^features](linkToPmBot.com)^^|other ^^info ^^here")
        '''
        comment.reply(message+"^^[meta][^^See ^^all ^^my ^^commands](wikilinkhere.com)^^|[suggest ^^new ^^features](linkToPmBot.com)^^|other ^^info ^^here")
        '''
        #is there a way to do the ^^ effect without having to do it before every word?
        
    #rolls dice and saves each roll in an array, total of the rolls is at the end of the array. This is done so that a table of the rolls can be made if needed.
    #command can be '!roll 5d6' or something like that
    #ready for initial usage in the bot - can be upgraded later
    def rollDice(amnt, sides):
        total = 0
        rolls = []
        for i in range(0,amnt):
            del i
            roll = random.randrange(sides)+1 
            total+=roll
            rolls.append(roll)
        rolls.append(total)
        global message
        message+="You roll "+str(amnt)+" dice with "+str(sides)+" sides each.\nYour total is **"+str(rolls[len(rolls)-1])+"**\n___\n"
    
    #makes a cake, probably won't use this actual method in the final code as it's so short
    #command can be '!cake' or something like that, or you mentioned something about it being taken under verbage
    #ready for initial usage in the bot - can be upgraded later
    def cake():
        global message
        message+="Here is your cake sir:\n     ,,,,,\n    _|||||_\n   {~*~*~*~}\n __{*~*~*~*}__\n`-------------`\n___\n"
    
    #this is the welcome message. Will be replied to posts of users that have never posted before
    #ready for initial usage in the bot - can be upgraded later
    def welcome():
        global message
        message+=welcomeMessage+'\n'
        refreshMemory()
        
    #this is the second part of the welcome message that peopl can ask for on demand
    def refreshMemory():
        global message
        message+=refreshMessage+'\n___\n'
        
    #Call everything the bot needs to do here, then write the code above
    while True:
        checkForCommands()
        cake()
        rollDice(2,6)
        welcome()
        refreshMemory()
        commentReply()
        time.sleep(10)
except:
    print('Error')
    time.sleep(30) #we can change the time to whatever