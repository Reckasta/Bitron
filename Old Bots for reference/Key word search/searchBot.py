'''
Created on Nov 16, 2015

@author: Mjone77
'''
import praw
import time
import winsound
import writing
import sys
import configparser

try:
    config = configparser.ConfigParser()
    config.read('searchConfig.ini')
    checkNum = int(config['Technical']['threads to check'])
    sub = config['General']['subreddit']
    errorDelay = int(config['Technical']['error delay'])
    normalDelay = int(config['Technical']['seconds between checks'])
    triggers = config['Triggers']['trigger words'].lower().split(',')
    triggerFlairs = config['Triggers']['trigger flair'].lower().split(',')
    soundAlert = (config['General']['sound alert']).lower()
    excludedSubs = config['General']['excluded subreddits'].lower().split(',')
except:
    config = configparser.ConfigParser()
    config['General'] = {'subreddit': 'all',
                          'sound alert':'true',
                          'excluded subreddits':'giveaways'}
    config['Triggers'] = {'trigger words': 'giveaway,give away',
                          'trigger flair':'giveaway',}
    config['Technical'] = {'seconds between checks':'2',
                          'threads to check':'50',
                          'error delay':'30',}
    with open('searchConfig.ini','w') as configfile:
        config.write(configfile)
    print("Please complete generated searchConfig.ini")
    sys.exit()
r = praw.Reddit('Searches for keywords/flairs')
title = "logs\serachLog "+time.strftime("%Y-%m-%d %H.%M.%S")+'.txt'
alreadyUsed = []
titleChecked = []
writing.writeToFile(title,"Starting in /r/"+sub)
n = 0
while True:
    n+=1
    try:
        subreddit = r.get_subreddit(sub)
        x = 0
        for submission in subreddit.get_new(limit=checkNum):
            flair = str(submission.link_flair_css_class).lower()
            submissionTitle = submission.title.lower()
            alert = False
            if (submission.id not in alreadyUsed and submission.subreddit._case_name.lower() not in excludedSubs):
                if(submission.id not in titleChecked):
                    notDone = True
                    for trigger in triggers:
                        if(trigger in submissionTitle and notDone):
                            alert = True
                            notDone = False
                    titleChecked.append(submission.id)
                if(triggerFlairs[0]!='' and flair in triggerFlairs):
                    alert = True
            if(alert):
                writing.writeToFile(title, "Found in "+submission.subreddit._case_name+" titled \""+submissionTitle+"\" "+submission.short_link)
                if(soundAlert=='true'):
                    winsound.PlaySound("H:\Documents\Programs & Stuff\Sounds\hldj sounds\GabeN_song.wav", winsound.SND_FILENAME)
                alreadyUsed.append(submission.id)
                x+=1
        print(str(n)+" Searched "+str(checkNum)+" threads, found "+str(x))
        time.sleep(normalDelay)
    except Exception as e:
        writing.writeToFile(title,"ERROR ): "+str(e))
        time.sleep(errorDelay)
        writing.writeToFile(title,"Resuming")
        x-=1
