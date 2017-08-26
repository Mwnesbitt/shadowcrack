#!/usr/bin/python3
# Mark Nesbitt
# 20170810
# Applies a dictionary attack based on a wordlist specified by user input against a Linux shadow file specified by user.

import crypt
import os
import sys
import re

def get_lists(dictfile, hashfile):
    #print(dictfile)
    #print(hashfile)
    
    wordslist = []
    pwslist = []
    try:
        wordsf= open(dictfile,'rb')
        wordslist = wordsf.read().splitlines()
        wordsf.close()
    except:
        print("That words file doesn't exist")
        sys.exit(1)
    try:
        pwsf = open (hashfile, 'r')
        pwslist = pwsf.readlines()
        pwsf.close()
    except:
        print("That passwords file doesn't exist")
        sys.exit(1)
    
    newwordslist = []
    for item in wordslist:
        try:
            newwordslist.append(str(item, encoding='UTF-8'))
        except:
            pass
    #print(newwordslist)
    #print(pwslist)
    return newwordslist, pwslist

def parse_hashes(hashrow):
    user = ''
    salt = ''
    hashedpw = ''
    
    rowlist = hashrow.split(':')
    #print(rowlist) 
   
    user = rowlist[0]
   
    match = re.search("(\$\d\$.*\$)(.*)",rowlist[1])
    salt = match.group(1)
    pwhash = match.group(2)
    
    return user, salt, pwhash

    
def main():
    words, pwslist = get_lists(sys.argv[1], sys.argv[2])
    #print(pwslist) 
    results = []
    for item in pwslist:
        user, salt, pwhash = parse_hashes(item) 
        #print(user, salt, pwhash)
        counter = 0 
        for password in words:
            print(counter)
            counter+=1
            #print(password)
            candidate = crypt.crypt(str(password),salt)[12:] 
            #print(candidate)
            #print(pwhash)
            if candidate == pwhash:
                print(user+"'s password is "+password)
                f = open("cracker_"+user+".txt", 'w')
                f.write(user+":"+salt+password)
                f.close()
                #results.append((user, salt, password))
                break
        #results.append((user, "password not found"))
    #print(results)

if __name__ == '__main__':
    main()
