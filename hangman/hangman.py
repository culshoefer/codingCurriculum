######################################################
#######################################################
##                                                   ##
##             DO NOT CHANGE ANYTHING HERE           ##
##                                                   ##
#######################################################
#######################################################

import sys
import random

words = ["Hangman",
         "Potato",
         "Blackboard",
         "Skyscraper",
         "Python"]


DEAD = False
TRY = 12

word = random.choice(words).lower()
solved = []

while not DEAD:

    print ('Guesses left: ' + str(TRY))
    print 

    s = ''
    for c in word:
        if c not in solved:
            s += '_'
        else:
            s += c 
    
    print (s)
    if s == word:
        print 'You WIN'
        quit()
    
    print 
    
    c = ''
    while c == '' or c in solved:
        c = raw_input('Guess a character: ')[0]

    #######################################################
    ##                                                   ##
    ##              ADD YOUR CODE HERE                   ##
    ##                                                   ##
    #######################################################

    # check whether the character c is in the list word,
    # if it is in the list word, add the character c to the list
    # otherwise decrease the variable TRY by 1 and check,
    # whether the player can continue playing, i.e. if he has TRY's left
    # if not, you should set DEAD to true and print a message, that the player 
    # lost

    if c in word:
        solved.append(c)
    else:
        TRY -= 1
        if TRY <= 0:
            DEAD = True
            print('You lost')
