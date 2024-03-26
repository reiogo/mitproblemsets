#!/usr/bin/env python3

# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <Ray O>
# Collaborators : <your collaborators>
# Time spent    : <4 days>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

# add in wildcard value = 0
SCRABBLE_LETTER_VALUES = {
        '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    # sum of the letter points
    w = word.lower()
    sum_points = 0
    for l in w:
        sum_points += SCRABBLE_LETTER_VALUES[l]
    # multiplier calculations
    wordlen = len(word)
    multiplier = 7*wordlen - 3*(n-wordlen)
    score = 0
    if multiplier>1:
        score = multiplier*sum_points
    else:
        score = 1*sum_points
    return score





#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                             # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    # for wildcard
    hand['*'] = hand.get('*', 0) +1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 


    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # word should be lowercase
    w = word.lower()
    # Remove letter of word from the hand using handlist as an intermediate
    handlist = []
    update_hand = hand.copy()
    pass  # TO DO... Remove this line when you implement this function
    for l in w:
        for i in hand.keys():
            if l == i:
                handlist.append(l)
    for r in handlist:
        if update_hand[r] >= 1:
            update_hand[r] = update_hand.get(r,0) - 1
    return update_hand




#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    # remove case sensitivity, see if the word is in the word_list, allow for wildcard
    w = word.lower()
    flag = 0
    for e in word_list:
        e = e.lower()
        if w == e:
            flag += 1
            break 
        if '*' in w:
            for v in VOWELS:
                w_ = list(w)
                w_[w.find('*')] = v 
                w_ = ''.join(w_)
                if w_ == e:
                    flag += 1
                    break
    if flag == 0:
        return False
    # Checking if the word is made of letters from the hand
    temp_word = list(w)
    temp_hand = hand.copy()
    counter = 0
    for e in word:
        e = e.lower()
        if temp_hand.get(e,0)>= 1:
            temp_hand[e]=temp_hand.get(e,0)-1
            temp_word.remove(e)
            counter+=1
    if temp_word==[]:
        return True
    else:
        return False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count = 0
    for r in hand.keys():
        if hand.get(r,0)>0:
            count+= hand.get(r,0)
    return count


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # Keep track of the total score
    total_score = 0    
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand)>0:
        # Display the hand
        print('Current Hand: ', end = ' ') 
        display_hand(hand)
        print()
        # Ask user for input
        word = input('Enter word or \"!!\" to indicate that you are finished: ') 
        # If the input is two exclamation points:
        if word == '!!': 
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):            
                # Tell the user how many points the word earned,
                # and the updated total score
                total_score += get_word_score(word, calculate_handlen(hand))
                print('\"', word,'\" earned', get_word_score(word, calculate_handlen(hand)),' points. Total :', total_score)
                print()
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print('That is not a valid word. Please choose another word.')     
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word) 

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if word != '!!':
        print('Ran out of letters')
    print('total score for this hand: ', total_score, 'points')
    print('------------')
    print() 
    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # create copy of hand
    w = hand.copy()
    # if letter not in hand
    if letter not in w:
        # return copy of hand
        return w
    # else (letter is in hand)
    else:
        # choose random letter
        q = random.choice(CONSONANTS+VOWELS)
        # while random letter is in hand
        while q in w:
            # choose different letter
            q = random.choice(CONSONANTS+VOWELS)
        # add key with random letter and value equal to letter
        w[q] = hand.get(letter, 0)
        # delete key/value with letter
        del w[letter]
        # return copy of hand
        return w

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    # Ask for input: how many hands
    h = int(input('Enter total number of hands: '))
    # initialize counters for substitutions and replay
    subcounter = 0
    replaycounter = 0
    # initialize score
    gamescore = 0
    # repeat for however many hands there are
    for x in range (h):
        # print current hand
        hand = deal_hand(HAND_SIZE)
        print('Current hand is: ', end = '')
        display_hand(hand)
        print()
        # if counter for substitution is zero
        if subcounter == 0:
            # ask if user wants to sub a letter (while loop, case insensitive)
            ans = input('Would you like to substitute a letter? ')
            print()
            ans = ans.lower()
            while ans != 'yes' and ans != 'no':
                ans = input('Your answer wasn\'t in the right form, type yes or no: ')
            # if answer is yes
            if ans == 'yes':
                # ask what letter they want to sub (while loop)
                subletter = input('Which letter would you like to replace? ')
                subletter = subletter.lower()
                # substitute letter
                hand = substitute_hand(hand, subletter)
                # add to counter
                subcounter += 1
        # play a hand and assign a variable to the returned value
        hand_score = play_hand(hand, word_list)
        # if replay counter is zero 
        if replaycounter == 0:
            # ask if user wants to replay (while loop)
            replayans = input('Would you like to replay the hand? ')
            replayans = replayans.lower()
            while replayans != 'yes' and replayans!= 'no':
                replayans = input('Your answer wasn\'t in the right form, type yes or no: ')
            # if answer is yes
            if replayans == 'yes':
                # get a new hand
                hand = deal_hand(HAND_SIZE)
                display_hand(hand)
                # play hand again and assign the returned value a different variable
                second_score = play_hand(hand, word_list)
                # if second play returns higher score
                if second_score > hand_score:
                    # the replay score becomes the main score
                    hand_score = second_score
                # add to counter
                replaycounter += 1
        # the score from this iteration is added to the overall score
        gamescore += hand_score
    # show and return the overall score
    print('Total score over all hands: ', gamescore)
    return gamescore              




#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
