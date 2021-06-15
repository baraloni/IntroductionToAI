307944017
305230740
*****
Comments:
Q5: The evaluation function we used is a linear combination of the following: 
	* Number of empty tiles: We want the game to continue on and on ( so we'll have
				a better chance at improving our score). Therefore we would
				like to take into considiration the number of empty tiles.
				(between 0 and 16)
	* Merge potential: In order to describe our game state better then just to look at the
			   Number of empty tiles, we will consider the merging potential this
			   board holds. In this way we will favor the states which can be reduced
			   (and earn us a certain amount of points along the way) among the ones 
			   that has the same number of free tiles.
	* Smoothness: We will fine states by their lake of "smoothness": the difference between 
		      the values in adjecent tiles.
		      We will do so in accordance to the smoothness level so we can favor
		      states that will be "easier" to merge in a few steps time. 
 		      We've also normalized the penalty with the value of the max tile, in order to 
		      keep conssistent evaluation scores.


    The process of finding the optimal weights for the liear combination was made by a CMA-ES learner: 
    a stochastic, derivative-free methods for numerical optimization of non-linear or non-convex continuous 
    optimization problems.