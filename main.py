'''
This is a reddit bot coded by
/u/Mjone77
'''
import time
import praw
import random
import sys
import configparser
import OAuth2Util

print('running')
while True:
    #this try/except is suppose to surround the whole thing to prevent crash even if some major error occurs that we overlooked
    try:
        #This sets up the variables and junk from the ini file, also creates an ini file if it is missing
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            welcomeMessageLines = config['Welcome']['message'].split('`^')
            refreshMessageLines = config['Welcome']['refresh'].split('`^')
            admins = config['Admin']['users'].split(',')
            alreadyReplied = config['Technical']['alreadyReplied'].split(',')
            alreadyWelcomed = config['Technical']['alreadyWelcomed'].split(',')
        except Exception as e:
            print(str(e))
            config = configparser.ConfigParser()
            config['Welcome'] = {'message': 'Welcome!',
                                 'refresh': 'Refresh'}
            config['Admin'] = {'users': ''}
            config['Technical'] = {'alreadyReplied': '',
                                   'alreadyWelcomed': ''}
            with open('config-new.ini','w') as configfile:
                config.write(configfile)
            print("Please complete generated config-new.ini")
            sys.exit()
        
        #log's on to reddit here and set the subreddit
        r = praw.Reddit('who really cares what goes here???')
        o = OAuth2Util.OAuth2Util(r)
        o.refresh(force=True)
        subreddit = r.get_subreddit('subreddit')
        message = "" #add replies to this. Make sure to add a \n___\n (3 underscores) after every message. Hopefully this will allow multiple commands to be called with one comment
        needSave = False
        welcomeMessage = ''
        refreshMessage = ''
        for line in welcomeMessageLines:
            welcomeMessage+=line+'\n\n'
        for line in refreshMessageLines:
            refreshMessage+=line+'\n\n'
        messageEnd = "[meta][See all my commands](http://subreddit.wikia.com/wiki/FacilityAI)|[suggest new features](https://www.reddit.com/message/compose/?to=Mjone77&subject=FacilityAI_Suggestion)|[report bugs/errors](https://www.reddit.com/message/compose/?to=Mjone77&subject=FacilityAI_Report)"
        
        #Add comment or post id's to array and config.ini
        #idType: 0 is a comment.id, 1 is a username
        def addID(idToAdd, idType):
            if idType == 0:
                alreadyReplied.append(idToAdd)
                config['Technical']['alreadyReplied']+=(idToAdd+',')
            elif idType == 1:
                alreadyWelcomed.append(idToAdd)
                config['Technical']['alreadyWelcomed']+=(idToAdd+',')
            global needSave
            needSave = True
            
        #Checks the comments/posts/pm's for commands, and handles them
        def checkForCommands():
            global message
            recentComments = r.get_comments('subreddit')
            for comment in recentComments:
                if '!' in comment.body and str(comment.id) not in alreadyReplied and str(comment.author) != 'FacilityAI':
                    addID(str(comment.id), 0)
                    #print(str(comment.author)+'\n'+str(comment.body))
                    message = ''
                    commentLines = comment.body.lower().splitlines()
                    commentWords = []
                    for line in commentLines:
                        for word in line.split(' '):
                            commentWords.append(word)
                    if '!roll' in commentWords:
                        try:
                            numbers = commentWords[commentWords.index('!roll')+1].split('d')
                            rollDice(int(numbers[0]),int(numbers[1]))
                        except:
                            message+='[META]To roll dice, please use !roll followed by #d#, for example saying \"!roll 3d5\" would roll 3 dice with 5 sides each.\n___\n'
                    if '!cake' in commentWords:
                        cake()
                    if '!refresh' in commentWords:
                        refreshMemory()
                    if '!nowelcome' in commentWords and str(comment.author) not in alreadyWelcomed:
                        print(str(comment.author))
                        addID(str(comment.author),1)
                        message+='You have been registered as a veteran faculty member and will not be welcomed to work. Ever.\n___\n'
                    #print(message)
                    if message:
                        commentReply(comment)
            for submission in subreddit.get_new(limit=3):
                if str(submission.author) not in alreadyWelcomed:
                    addID(str(submission.author), 1)
                    message = ''
                    #welcome(submission)
                
            
        #Reply to comments
        def commentReply(comment): #Don't forget takes in comment
            print('replying')
            global message
            comment.reply(message+messageEnd)
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
            message+="You roll "+str(amnt)+" dice with "+str(sides)+" sides each.\n\nYour total is **"+str(rolls[len(rolls)-1])+"**\n___\n"
        
        #makes a cake, probably won't use this actual method in the final code as it's so short
        #command can be '!cake' or something like that, or you mentioned something about it being taken under verbage
        #ready for initial usage in the bot - can be upgraded later
        def cake():
            global message
            #message+="Here is your cake sir:\n\n      ,,,,,  \n     _|||||_  \n    {~\*~\*~\*~}  \n  __{\*~\*~\*~\*}__  \n `-------------`\n___\n"
            message+="Here is your cake sir:\n\n*tube descends from the ceiling and spits out a [cake](http://cakes-by-bill.com/images/birthday_pic5.jpg)*\n___\n"
        
        #this is the welcome message. Will be replied to posts of users that have never posted before
        #ready for initial usage in the bot - can be upgraded later
        def welcome(submission):
            global message
            message+=welcomeMessage+"\n"
            refreshMemory()
            submission.add_comment(message+messageEnd)
            
        #this is the second part of the welcome message that people can ask for on demand
        #ready for initial usage in the bot - can be upgraded later
        def refreshMemory():
            global message
            message+=refreshMessage+'\n___\n'
            
        #saves changes to config file
        def saveConfig():
            with open('config.ini','w') as configfile:
                config.write(configfile)

        #Tells me it started without error
        #print('Starting')
        #Call everything the bot needs to do here, then write the code #above
        checkForCommands()
        if needSave:
            print('saving')
            saveConfig()
            needSave = False
        time.sleep(10)

    except Exception as e:
        print(e)
        time.sleep(30) #we can change the time to whatever
