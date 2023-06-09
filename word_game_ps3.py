# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Hassan Kashif	
# Collaborators : N/A
# Time spent    : Unknown

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
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
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("Loading word list from file...", len(wordlist), "words loaded.\n")
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
    
    first_component = 0
    second_component = 1
    for letter in word:
        if letter.lower() in SCRABBLE_LETTER_VALUES.keys():
            first_component += SCRABBLE_LETTER_VALUES[letter.lower()]
    second_component_a = (7 * len(word) - 3 *(n-len(word)))
    if  second_component_a > 1:
        second_component = second_component_a
    word_score = first_component * second_component
    return word_score

# word = '*t'
# n = 2
# print(get_word_score(word, n))




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
    print()                              # print an empty line

# hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u': 1}
# display_hand(hand)

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
    
    i ='*'
    hand['*'] = hand.get('*', 0) + 1
    
    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    return hand

# print(deal_hand(5))
# a = display_hand(deal_hand(5))
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
    
    new_hand = hand.copy()
    updated_hand = {}
    # print(new_hand)
    
    for i in new_hand.keys():
        for j in word.lower():
            if i == j:
                new_hand[i] = new_hand.get(i, "No entry") - 1
    for k in new_hand.keys():
            if new_hand[k] != 0:
                updated_hand[k] = new_hand.get(k, 0) 
    return updated_hand  #or new_hand 
    

# word = 'Qualli'
# hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
# print(update_hand(hand, word))

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
    hand_copy = hand.copy()
    hand_check = []
    word_check_str = ''
    k = 0
    for i in word.lower():
        if i in hand_copy.keys() and hand_copy[i] != 0:
            hand_check.append(i)
            hand_copy[i] = hand_copy.get(i, "No entry") - 1
        if i == '*':
            for j in VOWELS:
                word_check_list = list(word.lower())
                word_check_list[k] = j
                word_check_str = ''.join(word_check_list)
                if word_check_str in word_list:
                    break
        k += 1
    hand_check_str = ''.join(hand_check)
    if word.lower() in word_list and word.lower() in hand_check_str:
        return True
    elif word_check_str in word_list and word.lower() in hand_check_str:
        return True
    else: 
        return False

# word = 'rapture'
# hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u': 1}
# print(is_valid_word(word, hand, load_words()))

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    n = 0
    for i in hand:
        if hand[i] != 0:
            n += 1
    return n

# hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u': 1}
# print(calculate_handlen(hand))


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
    score = 0
    n = 1
    # As long as there are still letters left in the hand:
    while n > 0: 
        # Display the hand
        print("\nCurrent Hand:", end = " " )
        display_hand(hand)
        # Ask user for input
        word = input("Enter word, or '!!' to indicate that you are finished: ")
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            n = 0
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list) == True:
                # Tell the user how many points the word earned,
                # and the updated total score
                score += get_word_score(word, n)
                print("'" + word + "'", "earned", get_word_score(word, n), "points. Total:", score)
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("This is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
            n = len(hand)
    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if word == '!!':
        print("\nTotal score for this hand:", score, "points")
    else:
        print("\nRan out of letters. Total score for this hand:", score, "points")
    # Return the total score as result of function
    return score

# word_list = load_words()
# hand = {'a': 1, 'c': 1, 'f': 1, 'i': 1, '*': 1, 't': 1, 'x': 1}
# play_hand(hand, word_list)


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand):
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
    
    flag = False
    letters_list =[]
    while flag == False:
        letter = input("Which letter would you like to replace: ")
        #If no, ask the question until a letter present in the hand is chosen
        if letter.lower() in hand:
            flag = True
        else:
            print("Enter a letter present in current hand.")
    #Note how many times the chosen letter appears in the user's hand
    n = hand[letter.lower()]
    #Delete the chosen letter from the user's hand
    del(hand[letter.lower()])
    #Make a list of letters not in the user's hand and not the substituted letter
    for i in string.ascii_lowercase:
        if i not in hand.keys() and i != letter.lower():
            letters_list.append(i) 
    #Pick a random letter from this list and add it to user's hand
    x = random.choice(letters_list)
    hand[x] = hand.get(x, 0) + n
    #Return new hand with substituted letter
    return hand

# letter = 'a'    
# hand = {'a': 1, 'c': 1, 'f': 1, 'i': 1, '*': 1, 't': 1, 'x': 1}
# substitute_hand(hand) 
   
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
    
    hands = int(input("Enter total number of hands: "))
    score = 0
    total_score = 0
    replay_n = 1
    replay_s = 1
    count = 1
    while hands > 0:
        print("\nThis is hand no.", count)
        replay = 0
        n = random.randint(4, 10)
        hand = deal_hand(n)
        display_hand(hand)  
        if replay_s > 0: 
            substitute = input("Would you like to substitute a letter? ")  
            if substitute.lower() == 'yes':
                substitute_hand(hand)
                replay_s -= 1  
        else:
            print("No substitutes available")
        while replay == 0:
            hand_n = hand
            score = play_hand(hand_n, word_list)
            if replay_n != 0:
                replay = input("Would you like to replay the hand? ")
                if replay.lower() == 'yes':
                    replay = 0
                    score = 0
                    replay_n -= 1
            else:
                replay = 1
            total_score += score  
        hands -= 1
        count += 1

    print("-"*10, "\nTotal score over all hands:", total_score)
    return 


def continue_function():
    while True:
        a = input("\nWould you like to run the program again? [Yes or No]: ")
        if a.lower() == "yes":
            print("\n", "-"*25,"-"*25)
            return 1
        elif a.lower() == "no": 
            print("\nProgram shutting down...\n", "-"*25,"-"*25)
            return 0
        else: 
            print("Enter a valid response!")
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement

if __name__ == '__main__':
    i = 1
    while i == 1:
        word_list = load_words()
        play_game(word_list)
        i = continue_function()

