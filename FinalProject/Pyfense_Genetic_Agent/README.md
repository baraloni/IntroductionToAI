Running instructions:
- Use "make run" command in your terminal.
- If something is missing, please run "make install" command.
- Demo run parameters are set to:
Genetic tested parameters:
POP_SIZE = 12
MUTATION_RATE = 0.1

Genetic constant parameters:
FITTEST_AMOUNT = 10
NUM_GENERATIONS = 3
MUTATION_RATE_MULTIPLIER = 5

Game constant:
NUM_SEGMENTS = 2  		# The number of game levels on which we want to learn
START_OF_GAME_MONEY = 500
INIT_WAVE = 1
MAX_EARNINGS_PER_SEGMENT = 1160
WAVES_PER_SEGMENT = 9
	
To change any of the algorithm's or game's parameters, go to AI_GENETIC_AGENT/GeneticAlgorithm/config.py