# Problem Set 2, hangman.py
# Name: Ray Ogoda 
# Collaborators: 
# Time spent: 1 night

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string


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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()








def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    correct = ''
    for l in secret_word:
        for m in letters_guessed:
            if l == m:
                correct += m
    return secret_word == correct 


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    unique_letters = ''
    for n in  letters_guessed:
        if str.isalpha(n) and n not in unique_letters:
            unique_letters += n
    current = ''
    for l in secret_word:
        for m in unique_letters:
            if m == l: 
                current+= m
        if l not in current:
            current+= '_ '
    return current


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available = ''
    for l in string.ascii_lowercase:
        if not (l in letters_guessed):
            available += l
    return available



def check(i,letters_guessed):
    ''' 
    Enter value 
    Check if the value is in alphabet, return lowercase of string otherwise print error statements(not_valid or already_guessed) 
    ''' 
    not_valid = 'not_valid'
    already_guessed = 'already_guessed'
    space = 'space'
    star = 'star'
    try:
        if i in letters_guessed:
            return already_guessed
        elif i == '':
            return space 
        elif i == '*':
            return star
        elif not str.isalpha(i):
            return not_valid 
        elif str.isalpha(i):
            str.lower(i)
            return i
    except: 
        raise ValueError("the check has told me that the input wasn't valid")
        return not_valid



def prompt(guess, guesses_remaining, letters_guessed, warnings, secret_word):
    if guesses_remaining>0:
        print('You have ', guesses_remaining, 'guesses left.')
    else:
        print('You\'re on your last guess')
    print('Available letters: ', get_available_letters(letters_guessed))
    try:
        if guess =='already_guessed':
            print('Oops! You\'ve already guessed that letter. You now have ', warnings, ' warnings:', get_guessed_word(secret_word, letters_guessed))
        elif guess =='not_valid':
            print('Oops! That is not a valid letter. you have ', warnings ,' warnings left: ', get_guessed_word(secret_word, letters_guessed)) 
        elif guess == 'star':
            print('Possible word matches are:')
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        elif guess == 'space':
            print('Oops! Did you mean to enter a letter?')
        elif guess not in secret_word: 
            print('Oops! That letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
        elif guess in secret_word:
            print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
    except TypeError:
        raise TypeError('something has gone wrong in the prompt')
    print('------------')




def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    starts up an interactive game of hangman.
    
    * at the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * the user should start with 6 guesses

    * before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * ask the user to supply one guess per round. remember to make
      sure that the user puts in a letter!
    
    * the user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * after each guess, you should display to the user the 
      partially guessed word so far.
    
    follows the other limitations detailed in the problem write-up.
    '''
    numletters = 0
    guesses_remaining = 6
    letters_guessed = []
    warnings = 3
    score = 0
    loopcount=0
    print ('Welcome to the game Hangman!')
    for i in secret_word:
       numletters+=1 
    print('I am thinking of a word that is ', numletters, ' letters long') 
    print('------------')
    while guesses_remaining >= 0 and not is_word_guessed(secret_word, letters_guessed):
        if loopcount==0:
            prompt(None,guesses_remaining, letters_guessed, warnings,secret_word)
        guess = (check(input('Please guess a letter: '),letters_guessed))
        if len(guess)==1:
            letters_guessed += guess
        if guess == 'already_guessed':
            warnings -= 1
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess == 'not_valid' or guess == 'star':
            guess = 'not_valid'
            warnings -= 1
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess == 'space':
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess not in secret_word:
            if guess in 'aeiou':
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess in secret_word: 
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        if warnings == 0:
            guesses_remaining -= 1
            warnings += 3
        loopcount+=1
    if is_word_guessed(secret_word, letters_guessed):
        score = guesses_remaining*numletters
        print('Congratulations, you won!\nYour total score for this game is: ', score)
    elif guesses_remaining < 0:
        print ('Sorry, you ran out of guesses. The word was ', secret_word)



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_ns=my_word.replace(' ', '')
    not_in_myword=''
    already_in_myword=''
    flag=''
    if len(other_word) == len(my_word_ns):
        for l in range(len(other_word)):
            if other_word[l] == my_word_ns[l]:
                if other_word[l] in not_in_myword:
                    return False
                else:
                    flag+=other_word[l]
                    already_in_myword += other_word[l]
            elif my_word_ns[l] == '_':
                if other_word[l] in already_in_myword:
                    return False
                else:
                    flag+=other_word[l]
                    not_in_myword += other_word[l]
        if flag == other_word:
            return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []
    for m in wordlist:
        if match_with_gaps(my_word, m):
            matches.append(m)
    if matches != []:
        return matches
    else:
        return 'No matches found'


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    numletters = 0
    guesses_remaining = 6
    letters_guessed = []
    warnings = 3
    score = 0
    loopcount = 0
    print ('Welcome to the game Hangman!')
    for i in secret_word:
       numletters += 1
    print('I am thinking of a word that is ', numletters, ' letters long') 
    print('------------')
    while guesses_remaining >= 0 and not is_word_guessed(secret_word, letters_guessed):
        if loopcount==0:
            prompt(None,guesses_remaining, letters_guessed, warnings, secret_word)
        guess = (check(input('Please guess a letter: '),letters_guessed))
        if len(guess)==1:
            letters_guessed += guess
        if guess == 'already_guessed':
            warnings -= 1
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess == 'not_valid':
            warnings -= 1
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess == 'star':
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess == 'space':
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess not in secret_word:
            if guess in 'aeiou':
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        elif guess in secret_word: 
            prompt(guess,guesses_remaining, letters_guessed, warnings, secret_word)
        if warnings == 0:
            guesses_remaining -= 1
            warnings += 3
        loopcount+=1
    if is_word_guessed(secret_word, letters_guessed):
        score = guesses_remaining*numletters
        print('Congratulations, you won!\nYour total score for this game is: ', score)
    elif guesses_remaining < 0:
        print ('Sorry, you ran out of guesses. The word was ', secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
