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

#This sets up the variables and junk from the ini file, also creates an ini file if it is missing
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    welcomeMessageLines = config['Welcome']['message'].split('`^')
    refreshMessageLines = config['Welcome']['refresh'].split('`^')
    admins = config['Admin']['users'].lower().split(',')
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
subreddit = r.get_subreddit('secretsubreddit')
message = "" #add replies to this. Make sure to add a \n___\n (3 underscores) after every message. Hopefully this will allow multiple commands to be called with one comment
needSave = False
welcomeMessage = ''
refreshMessage = ''
tempRefresh = ''
needConfirmRefresh = False
for line in welcomeMessageLines:
    welcomeMessage+=line+'\n\n'
for line in refreshMessageLines:
    refreshMessage+=line+'\n\n'
messageEnd = "[meta][See all my commands](http://secretsubreddit.wikia.com/wiki/FacilityAI)|[suggest new features](https://www.reddit.com/message/compose/?to=Mjone77&subject=FacilityAI_Suggestion)|[report bugs/errors](https://www.reddit.com/message/compose/?to=Mjone77&subject=FacilityAI_Report)"

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
    recentComments = r.get_comments('secretsubreddit')
    #Checks for commands in comments
    for comment in recentComments:
        analyzeText(comment)
    #checks for commands in pm's
    for comment in r.get_unread(unset_has_mail=True, update_user=True):
        analyzeText(comment)
    for submission in subreddit.get_new(limit=3):
        if str(submission.author) not in alreadyWelcomed:
            addID(str(submission.author), 1)
            message = ''
            #welcome(submission)

#searches for possible commands in a comment/pm, then passes them on to be searched and replied to
def analyzeText(comment):
    global message
    if '!' in comment.body and str(comment.id) not in alreadyReplied and str(comment.author) != 'FacilityAI':
        addID(str(comment.id), 0)
        searchForCommands(comment.body, comment.author)
        if message:
            commentReply(comment)
            message = ''
        
#searches a string for commands
def searchForCommands(body, author):
    global message
    global admins
    message = ''
    commentLines = body.lower().splitlines()
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
    if '!encrypt' in commentWords:
        try:
            msg = body[body.lower().find('!encrypt'):len(body)].split('"')[1]
            offset = int(body[body.lower().find('!encrypt')+9:len(body)].split(' ')[0])
            message+=a1z26(offset,msg)+'\n___\n'
        except:
            message+='In order to encrypt a message, please comment like this:\n!encrypt offset "message to encrypt"\nOffset is a number, normally 0. The message must be surrounded by ", this allows you continue your comment past the command if you\'d like\n___\n'
    if '!decrypt' in commentWords:
        try:
            msg = body[body.lower().find('!decrypt'):len(body)].split('"')[1]
            offset = int(body[body.lower().find('!decrypt')+9:len(body)].split(' ')[0])
            message+=a1z26Rev(offset,msg)+'\n___\n'
        except:
            message+='In order to decrypt a message, please comment like this:\n!decrypt offset "message to decrypt"\nOffset is a number, normally 0. The message must be surrounded by ", this allows you continue your comment past the command if you\'d like\n___\n'
    if '!nowelcome' in commentWords and str(author) not in alreadyWelcomed:
        print(str(author))
        addID(str(author),1)
        message+='You have been registered as a veteran faculty member and will not be welcomed to work. Ever.\n___\n'
    if str(author).lower() in admins:
        global needConfirmRefresh
        global tempRefresh
        global needSave
        if needConfirmRefresh:
            if '!confirmrefresh' in commentWords:
                try:
                    global refreshMessage
                    config['Welcome']['refresh'] = tempRefresh
                    refreshMessageLines = tempRefresh.split('`^')
                    refreshMessage = ''
                    for line in refreshMessageLines:
                        refreshMessage+=line+'\n\n'
                    needSave = True
                    needConfirmRefresh = False
                    message+='Refresh updated.\n___\n'
                    refreshMemory()
                except:
                    message+='Something went wrong when attempting to update the Refresh message, please try again. Refer to the wiki for a guide on how to update the message or pm /u/Mjone77 if you have any questions.\n___\n'
        if '!updaterefresh' in commentWords:
            try:
                tempRefresh = body[body.lower().find('!updaterefresh'):len(body)].split('"')[1]
                msg = tempRefresh.split('`^')
                sampleRefresh = ''
                for line in msg:
                    sampleRefresh+=line+'\n\n'
                needConfirmRefresh = True
                message+='The refresh message will be set to this once you reply with !confirmRefresh:\n___ \n\n'+sampleRefresh+'\n___\n'
            except:
                message+='Something went wrong when attempting to update the Refresh message, please try again. Refer to the wiki for a guide on how to update the message or pm /u/Mjone77 if you have any questions.\n___\n'    
        if '!refreshsource' in commentWords:
            message+=config['Welcome']['refresh']+'\n___\n'
        if '!addadmin' in commentWords:
            try:
                if commentWords[commentWords.index('!addadmin')+1] not in admins:
                    admins+=commentWords[commentWords.index('!addadmin')+1]
                    tempAdmins = ''
                    for name in admins:
                        tempAdmins+=name+','
                    config['Admin']['users'] = tempAdmins
                    needSave = True
                message+='The admins are now:\n\n'+str(admins)+'\n___\n'
            except:
                message+='Something went wrong, please make sure your command looks like this:\n\n!addAdmin name\n___\n'
#Reply to comments
def commentReply(comment): #Don't forget takes in comment
    print('replying\n'+comment.body)
    global message
    comment.reply(message+messageEnd)
    #is there a way to do the ^^ effect without having to do it before every word?
    
#rolls dice and saves each roll in an array, total of the rolls is at the end of the array. This is done so that a table of the rolls can be made if needed.
#command can be '!roll 5d6' or something like that
#ready for initial usage in the bot - can be upgraded later
def rollDice(amnt, sides):
    total = 0
    #rolls = []
    for i in range(0,amnt):
        del i
        roll = random.randrange(sides)+1 
        total+=roll
        #rolls.append(roll)
    #rolls.append(total)
    global message
    isPluralDice = ' die '
    isPluralSides = ''
    if amnt != 1:
        isPluralDice = ' dice '
        isPluralSides = ' each'
    message+="You roll "+str(amnt)+isPluralDice+"with "+str(sides)+' sides'+isPluralSides+".\n\nYour total is: **"+str(total)+"**\n___\n"

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
        
#Takes in a number and makes it between 1 and 26, used for a1z26
def valueBetween1And26(num):
    while(num<1 or num>26):
        if num>26:
            num-=26
        elif num<1:
            num+=26
 
#encrypts a string into a1z26 using an offset to shift the numbers around           
def a1z26(offset, msg):
    letters = list(msg.upper())
    nums = ""
    for let in letters:
        if not(ord(let)>64 and ord(let)<91):
            if nums[len(nums)-1] is '-':
                nums = nums[0:len(nums)-1]+let
            else:
                nums = nums[0:len(nums)]+let
        else:
            num = ord(let)-64+offset
            valueBetween1And26(num)
            nums = nums+str(num)+'-'
    if nums[len(nums)-1] is '-':
        return nums[0:len(nums)-1]
    else:
        return nums

#Decrypts a1z26
def a1z26Rev(offset, msg):
    nums = list(msg.upper())
    lets = ''
    realNum  = ''
    isNum = False
    for num in nums:
        try:
            int(num)
            isNum = True
        except:
            isNum = False
        if isNum:
            realNum = realNum+num
        else:
            if realNum:
                finalNum = int(realNum)-offset
                valueBetween1And26(finalNum)
                lets = lets+str(chr(finalNum+64))
                realNum = ''
            if num is not '-':
                lets = lets+num
    if isNum:
        finalNum = int(realNum)-offset
        valueBetween1And26(finalNum)
        lets = lets+str(chr(finalNum+64))
    return lets

#Tells me it started without error
print('Starting')
#Call everything the bot needs to do here, then write the code above
while True:
    try:
        checkForCommands()
        if needSave:
            print('saving')
            saveConfig()
            needSave = False
        time.sleep(10)
    except Exception as e:
        print(e)
        time.sleep(30) #we can change the time to whatever
