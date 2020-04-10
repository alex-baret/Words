# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Alex Baret
# Collaborators : None
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7 #players "hand" of letters chosen randomly, may include instances of same letter
#player makes as many words as possible with this hand but only uses each letter once
#size of hand when word is played affects the score

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
} #score of each letter (same as scrabble)

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
    
    word_length = len(word)
    
    #----- First Component of Score ----#
    score_part_1 = 0 #initialize score variable part 1 at zero
    for char in word:#at this point entry is a valid word, iterate through the letters in the string
        if char == '*':
            score_part_1 += 0
        else:
            score_part_1 += SCRABBLE_LETTER_VALUES[char.lower()]#if it's a valid letter, lowercase it, add the points to score variable part 1
    # print(score_part_1)
    
    #----- Second Component of Score ----#
    score_part_2 = 0 #initialize score variable part 2 at zero
    #n has already been calculated and entered as an argument here
    #n would be num_letters = HAND_SIZE - word_length
    
    # ------- Check back to see if word_length needs to be calculated here ------- #
    calc = (7*word_length) - (3*(n-word_length))
    opt_1 = 1
    if calc > 1:#write conditional for second part being either (whichever is greater): 
        score_part_2 += calc #1) 7*word_length - 3*(n-word_length)
    else:
        score_part_2 += opt_1 #2) the value of 1
    # print(score_part_2)
    
    #----- First and Second Component of Score Calculated ----#
    score = score_part_1*score_part_2
    return score#return an int of the score
    
    
    
    
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
    hand.update({'*': 1}) #adds wildcard value to hand
    num_vowels = int(math.ceil((n-1) / 3)) #takes n-1 and divides by 3, rounds up to ceiling and that's # of vowels to get
    # print(num_vowels)
    for i in range(num_vowels): #for loop to get vowels
        x = random.choice(VOWELS)
        # print(x)
        hand[x] = hand.get(x, 0) + 1 #gets # of instances of x in dictionary, returns 0 if none, adds 1 to it 
        # print(hand)
        # print(num_vowels)
    for i in range(num_vowels, (n-1)): #for loop to get consonants (n-1 with addition of wildcard)
        x = random.choice(CONSONANTS)
        # print(x)
        hand[x] = hand.get(x, 0) + 1
        # print(hand)

    return hand

# test_hand = (deal_hand(7))
# display_hand(test_hand)
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
    
    origHand = hand #takes in original dict: hand
    # print(hand)
    origWord = word #takes in string word
    # print(word)
    updatedHand = origHand.copy()
    # print(updatedHand)
    for char in origWord.lower(): #iterates through word by each letter
        if char in updatedHand: #if the character in the word is in the dictionary then:
            updatedHand[char] -= 1 #reducing instance of letter in dictionary by one 
            if updatedHand[char] < 0:  #if value ends up being negative for a specific letter set it to 0
                updatedHand = 0
    returnedHand = []
    for i in updatedHand:
        if updatedHand[i] > 0:
            returnedHand.append(i)
    joinedHand = ''.join(returnedHand)
    # print(joinedHand)
    return updatedHand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):  #passes first four tests for wildcards, fails the last one
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    tempWord = word.lower()
    tempHand = hand.copy()
    wordlist = word_list
    if '*' in tempWord:
        listed_word = list(tempWord)
        index = listed_word.index('*')
        listed_word.remove('*')
        for char in VOWELS:
            listed_word.insert(index, char)
            tempWord2 = ''.join(listed_word)
            if tempWord2 in wordlist:
                return True
                break
            else:
                listed_word.remove(char)
        return False
    if tempWord not in wordlist:
        return False
    else:
        for char in tempWord:
            if char not in tempHand:
                return False    
                break
            if tempHand[char] <= 0:
                return False    
                break
            tempHand[char] -= 1
    return True


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    sum = 0
    for i in hand.values(): 
           sum = sum + i
           hand_len = sum
    return hand_len
    

def play_hand(hand, word_list): #sort of runs, doesn't calculate score correctly

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
   # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    total_score = 0 # Keep track of the total score
    
    while calculate_handlen(hand) >= 2: # As long as there are still letters left in the hand:
        print("Current Hand: ")# Display the hand
        display_hand(hand)
        word = input("Enter word, or !! to indicate that you are finished: ")# Ask user for input
        
        if word == '!!':# If the input is two exclamation points:
            break# End the game (break out of the loop)
        
        else: # Otherwise (the input is not two exclamation points):
            
            if is_valid_word(word, hand, word_list) == True: # If the word is valid:
                n = calculate_handlen(hand) #calculating n based off the length of the hand
                word_score = get_word_score(word, n) #gets single word score and stores in a variable
                print(word, "earned" , word_score, "points.")# Tell the user how many points the word earned,
                total_score += word_score #adds word score to total score
                print("Total score is: ", total_score, "points.")# and the updated total score   
            
            else: # Otherwise (the word is not valid):
                print("That is not a valid word. Please choose another word.")# Reject invalid word (print a message)               
            hand = update_hand(hand, word) # update the user's hand by removing the letters of their inputted word (valid or not)
            

    # Game is over (user entered '!!' or ran out of letters),
    print("Total score: ",total_score, "points.")# so tell user the total score

    return total_score# Return the total score as result of function



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
    copied_hand = hand.copy() #make a copy of orginal hand
    replace_let = letter #take in letter to be replaced 
    if replace_let not in copied_hand: #if letter to be replaced is not in the hand
        return copied_hand #exit the function and return the same hand
    if replace_let in copied_hand: #if the letter selected to be replaced is in the hand    
        alpha = '*aeioubcdfghjklmnpqrstvwxyz' #make a list of the alphabet 
        listed_alpha = list(alpha)
        for char in copied_hand.keys(): #iterate through hand dict to get each key value (letter)
            listed_alpha.remove(char) #takes the character out of list
            rejoined_alpha = ''.join(listed_alpha) #join list updated
        lenHand = calculate_handlen(copied_hand)
        while replace_let in copied_hand: #delete instances of the letter to be replaced from the hand
            del(copied_hand[replace_let])
        shorterHand = calculate_handlen(copied_hand)
        differenceHand = lenHand - shorterHand
        for i in range(differenceHand): #for loop going as long as the length of hand
            x = random.choice(rejoined_alpha) #randomly selects a vowel or consonant (either one)
            #copied_hand[x] = 1 #adds the random selection into the "substituted hand"
            copied_hand[x] = copied_hand.get(x, 0) + 1 #gets # of instances of x in dictionary, returns 0 if none, adds 1 to it #sum up the values of the dict and subtract it from n to get the length remaining

    return copied_hand #returns the substituted hand
    
    
    
           
    
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
    
    num_replays = 1 #store replay variable at 1 
    num_subs = 1 #store substitute variable at 1
    total_score = 0
    n = HAND_SIZE
    num_hands = int(input("How many hands would you like to play?")) #Take user input for number of hands to be played
    hand = deal_hand(n)
    display_hand(hand)
     # ----- Sub a Letter Section ------ #
    sub_opt = input("Is there a letter you'd like to substitute? (yes/no)") #take user input and give option to substitute a letter 
    if num_subs == 1 and 'yes' in sub_opt: #check if substitute variable is at 1
        num_subs -= 1
        sub_letter = input("Enter your letter to be substituted: ")
        subbed_hand = substitute_hand(hand, sub_letter)#invoke sub function 
        newHand_score = play_hand(subbed_hand, word_list)#continue hand play
        prev_score = newHand_score
        total_score += newHand_score
    # ------------------------------ #
    else:
        prev_score = play_hand(hand, word_list) #play first hand
        total_score += prev_score
    
    ######################## Game Loop After Hand 1 is played ###################
    for i in range(num_hands-1):#loop through play hand function for the number of iterations specified by user -1 (already played one)
        replay_option = input("Would you like to replay the last hand?") #Take user input asking whether they want to replay the previous hand
        if 'yes' in replay_option and num_replays == 1: #if yes check if replay variable is at 1:
            num_replays -= 1#subtract 1 from replay variable
            newHand_score = play_hand(hand,word_list) #replay the last hand 
            if newHand_score > prev_score: #if score from this replayed hand is greater than first try
                prev_score = newHand_score #overwrite the previous hand score or update total score to include this hand score in total score
                total_score += prev_score
        else:
           print("Your new hand is:")
           new_hand = deal_hand(n)
           display_hand(new_hand)
             # ----- Sub a Letter Section ------ #
           sub_opt = input("Is there a letter you'd like to substitute? (yes/no)") #take user input and give option to substitute a letter 
           if num_subs == 1 and 'yes' in sub_opt: #check if substitute variable is at 1
               num_subs -= 1
               sub_letter = input("Enter your letter to be substituted: ")
               subbed_hand = substitute_hand(new_hand, sub_letter)#invoke sub function 
               newHand_score = play_hand(subbed_hand, word_list)#continue hand play
               prev_score = newHand_score
               total_score += newHand_score
             # ------------------------------ #
           if num_subs != 1 and 'yes' in sub_opt:
               print("You cannot substitute a letter at this time.")  #let user know they already used it
               newHand_score = play_hand(new_hand,word_list) #play a new hand
               prev_score = newHand_score #update prev_score to most recent hand that's been played
               total_score += newHand_score  #add new hand score to total score
           else:
                newHand_score = play_hand(new_hand,word_list) #play a new hand
                prev_score = newHand_score #update prev_score to most recent hand that's been played
                total_score += newHand_score  #add new hand score to total score
    ######################## Game Loop After Hand 1 is played ###################

    print("Your total score for the series is: ",total_score)#print total score for the series of hands

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)