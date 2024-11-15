from random import shuffle
import matplotlib.pyplot as plt
import copy
from operator import add

def war():
    """
    The war function simulates a game of war between two players and keeps track
    of the number of occurrances of each player's size of possession (the size of 
    their hand + the size of their winning pile) and the number of wins and
    losses at each size of possession.

    There are no imput parameters for this function
    
    :return: [a_sizes,a_dubs]
        a_sizes is an ordered list of one player's size of possession
        a_dubs is a paraellel list to a_sizes and indicates whether the player 
        won or lost (1 or 0, respectively) at that size of possession
    """ 
    cards = [13, 13, 13, 13, 12, 12, 12, 12, 11, 11, 11, 11, 10, 10, 10, 10, 9, 9,
             9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 
             3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1]
    
    shuffle(cards)
    
    a_deck = cards[0:26]
    b_deck = cards[26:]
    a_dis = []
    b_dis = []
    a_sizes = []
    b_sizes = []
    a_dubs = []
    b_dubs = []
    collateral = []
    
    #While loop simulates the turn-based nature of the game
    while (len(a_deck) + len(a_dis)) > 0 and (len(b_deck) + len(b_dis)) > 0:
        #Checking if either player has run out of cards in their main deck, and
        #if so, shuffle their winning pile and use that as their deck
        if len(a_deck) == 0:
            shuffle(a_dis)
            a_deck = a_dis
            a_dis = []
        if len(b_deck) == 0:
            shuffle(b_dis)
            b_deck = b_dis
            b_dis = []
            
        #Designating the top card of each deck as the playing card
        a_playing = a_deck[0]
        b_playing = b_deck[0]
        
        #Adding the current size of possession to the first return list
        a_sizes.append(len(a_deck) + len(a_dis))
        b_sizes.append(len(b_deck) + len(b_dis))
        
        #Adding the playing cards to a list with the potential winnings of the
        #round, and removing those cards from each player's decks
        collateral.append(a_playing)
        collateral.append(b_playing)
        
        del a_deck[0]
        del b_deck[0]
        
        #Checking which player won, and adding the round winnings to their
        #winnings deck
        if a_playing > b_playing:
            for i in collateral:
                a_dis.append(i)
            collateral = []
            a_dubs.append(1)
            b_dubs.append(0)
        elif a_playing < b_playing:
            for i in collateral:
                b_dis.append(i)
            collateral = []
            a_dubs.append(0)
            b_dubs.append(1)
        #In the case of a tie, the round progresses to war
        else:
            a_dubs.append(0)
            b_dubs.append(0)
            #Checking if the first player has enough cards to go to war, then,
            #if they do, adding the cards to collateral, and if they don't have
            #enough cards, the game ends
            if len(a_deck) + len(a_dis) >= 3:
                if len(a_deck) >= 3:
                    for i in range(3):
                        collateral.append(a_deck[i])
                    del a_deck[0:3]
                else:
                    shuffle(a_dis)
                    for i in a_dis:
                        a_deck.append(i)
                    a_dis = []
                    for i in range(3):
                        collateral.append(a_deck[i])
                    del a_deck[0:3]
            else:
                break
            #The same check as above, and same action taken, but with the second
            #player
            if len(b_deck) + len(b_dis) >= 3:
                if len(b_deck) >= 3:
                    for i in range(3):
                        collateral.append(b_deck[i])
                    del b_deck[0:3]
                else:
                    shuffle(b_dis)
                    for i in b_dis:
                        b_deck.append(i)
                    b_dis = []
                    for i in range(3):
                        collateral.append(b_deck[i])
                    del b_deck[0:3]
            else:
                break

    return [a_sizes, a_dubs]

big_data = []
sizes = []
dubs = []
x_vals = list(range(1, 52))
y_vals = list(range(1, 52))
alt_y_vals = list(range(1, 52))
favourable = []
unfavourable = []
iters = 5000

#Creating a list of 51 zeros to store the number of wins and losses at the
#size of possession corresponding to the index (size - 1)
for i in range(0, 51):
    favourable.append(0)
    unfavourable.append(0)

#Playing war a set number of times and storing the data generated
for i in range(iters):
    big_data.append(war())

#Separating each list into size and dubs, each composed of an iters number of 
#lists for each game played
for i in big_data:
    sizes.append(i[0])
    dubs.append(i[1])

wins = copy.deepcopy(sizes)

#Working from the end to start of dubs to separate the wins (in the list 'wins')
#from the losses (in the list 'sizes'). Note each item of each original list
#is a list itself, which stores the data of each game, and there are 
for i in range(0, len(dubs)):
    for j in range(len(dubs[i]) - 1, -1, -1):
        if dubs[i][j] == 0:
            del wins[i][j]
        else:
            del sizes[i][j]

#Counting the number of wins and losses at each size of possession and assigning
#that number to the index of (number - 1)
for i in wins:
    for j in x_vals:
        favourable[j-1] += i.count(j)

for i in sizes:
    for j in x_vals:
        unfavourable[j-1] += i.count(j)

#Calculating the probability of a win or non-win at each deck size
for i in x_vals:
    y_vals[i-1] = favourable[i-1] / (favourable[i-1] + unfavourable[i-1])
    alt_y_vals[i-1] = unfavourable[i-1] / (favourable[i-1] + unfavourable[i-1])

#Plotting the total number of wins, non-wins, and occurances of each size of deck
plt.figure(1)
plt.plot(x_vals, list(map(add, favourable, unfavourable)), 'ko')
plt.plot(x_vals, unfavourable, 'ro')
plt.plot(x_vals, favourable, 'bo')
plt.xlabel("Size of Deck")
plt.ylabel("Total outcomes")
plt.legend(['Total', 'Non-wins', 'Wins'])
plt.title('Outcomes of a Single Player Based on Possessed Cards')

#Plotting the probability of a win
plt.figure(2)
plt.plot(x_vals, y_vals, 'bo')
plt.xlabel("Size of Deck")
plt.ylabel("Relative Probability")
plt.title('Relative Probability of a Win Based on Possessed Cards')

#Plotting the probability of a non-win
plt.figure(3)
plt.plot(x_vals, alt_y_vals, 'ro')
plt.xlabel("Size of Deck")
plt.ylabel("Relative Probability")
plt.title('Relative Probability of a Non-win Based on Possessed Cards')

plt.show()