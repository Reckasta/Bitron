'''
Created on Nov 18, 2015

@author: Mjone77
'''
import time

def writeToFile(title, text):
    try:
        file = open(title, 'a')
        file.write(time.strftime("\n%Y-%m-%d %H.%M.%S")+" "+text)
        file.close()
        print(time.strftime("\n%Y-%m-%d %H.%M.%S")+" "+text)
    except:
        file = open(title, 'a')
        file.write(time.strftime("\n%Y-%m-%d %H.%M.%S")+" Error writing to file")
        file.close()