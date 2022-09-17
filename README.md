# Sequence Game

My cousin approached me with a card game he was playing. He wanted to know the chance of winning, as he said that he was playing for a long time and couldn't win! So, to answer his question, I thought it would be quick and easy to set up a monte carlo simulaton of the game to generate a probability estimate.

The rules of the game are as follows:

1/ A standard deck of 52 cards is shuffled

2/ One by one, the player puts down a card and at the same time counts in the sequence 'Ace, 2, 3, 4, 5 ... Q, K'

3/ If, at any point, the same card is laid down as the number called, then that is a loss for the player

4/ If one count of 'Ace, 2, 3, 4, 5 ... Q, K' has passed without the same number card drawn, then the cycle is repeated again. This continues until the end of the deck

5/ If there is never the same number called and card laid down, then the player wins!

When writing the programme, I initially ran it for a certain number of steps to calclate the probaility as (number of wins)/(number of trials). I then thought it would be better to define some convergence criteria for the probability which the user can change - a stronger convergence results in a more accurate probability, but at the cost of longer computation time. To calculate an accurate probability though which does not fluctuate too much with number of iterations only requires a few seconds of computation time.

Also, every 5000 game-runs I sampled the number of wins in those 5000 games in order to sample the win probability, with aims of generating a distribution around the probability of wining this game, as I was curious to see the variance around how many wins someone can get. A roughly normal-looking histogram was the result so I performed some statistical tests to see the closeness of fit to a normal distrubution with the mean and variance obtained from the sampling.

