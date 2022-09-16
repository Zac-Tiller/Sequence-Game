import random
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
from scipy import stats

def shuffle_deck(deck):
    new_deck = random.sample(deck, len(deck))
    return new_deck


def set_up_hands():
    count_arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    deck_arr = np.array(list(count_arr) * 4)
    return deck_arr, count_arr


def fast_game(deck_arr, count_arr): # FULL GAME

    for i in range(2):
        deck_arr = shuffle_deck(list(deck_arr))

    bool_array = np.array(deck_arr) == np.array(list(count_arr)*4)

    if np.any(bool_array):
        player_looses = 1
    else:
        player_looses = 0

    return player_looses


def fast_sim(user_defined_error, error_difference):

    start = time.time()
    deck_arr, count_arr = set_up_hands()
    loose_counter = 0
    hist_loose_counter = 0
    win_distribution = [] # win distr is the prob of winning in 10,000 trials, sampled continously
    x = [0]
    y = [0]
    i = 0

    error = 1

    while np.abs(error - user_defined_error) > error_difference: # stop when error is within 1e-10 of user defined error
        i+=1

        if i % 5000 == 0: # sample every 5000 trials
            if i!= 0:
                win_distribution.append((5000 - hist_loose_counter)/5000)
                hist_loose_counter = 0

        if i % 50000 == 0:
            print('{} From Desired Error. Simulation Stops at Difference of < {}'.format((error - user_defined_error), error_difference))

        loose = fast_game(deck_arr, count_arr)
        loose_counter += loose
        hist_loose_counter += loose

        if i != 0:
            x.append(i)
            y.append(1 - loose_counter / i)

        if i < 1000: # burn in phase - otherwise the first x trials have a prob of loss of 1 so error is 0
            error = 1
        else:
            error = np.abs(y[i] - y[i-1])


    end = time.time()
    print('\n')
    print('TIME ELAPSED: {} seconds'.format(end - start))
    print('\n')

    probability_of_loosing = loose_counter/i
    probability_of_winning = 1 - probability_of_loosing
    print('Probability of winning: {}'.format(probability_of_winning))

    mean_p = np.mean(win_distribution)
    var_p = np.var(win_distribution)

    print('Mean probability from {} samples of 5000 games: {}'.format(i/5000, mean_p))
    print('Variance of probability from {} samples of 5000 games: {}'.format(i/5000, var_p))

    fitted_norm = stats.norm(loc=mean_p, scale=np.sqrt(var_p))
    stat, p_value = stats.kstest(win_distribution, fitted_norm.cdf)

    print('p-Value: {}'.format(p_value))

    if p_value < 0.05:
        print('p-Value < 0.05, so reject Null Hypothesis: the data are NOT Normally distributed')
    else:
        print('p-Value > 0.05, so accept Null Hypothesis (we cannot reject it): the data IS Normally distributed')

    print('\n')
    print('Odds = {}'.format(1/probability_of_winning))

    plt.plot(x,y)
    plt.title('Evolution of Win Probability With Simulation Number')
    plt.xlabel('Number of Games Simulated')
    plt.ylabel('Probability of Player Winning (ie. no match with card and number called)')
    plt.show()

    # plt.hist(win_distribution, bins=10)
    # plt.show()

    sns.displot(data=win_distribution, kde=True)
    plt.show()


fast_sim(1e-09, error_difference=5e-10) # error - this number < 5e-10 - ie the error has to be within 1e-10 of this number

