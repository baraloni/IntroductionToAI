from GeneticAgent.genetic_resources import Tower
import os

# running vars:
RUN_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))), "Pyfense_Genetic_Agent", "AI_PYFENSE", "Pyfense", "pyfense.py")
MODE = "learn"
# MODE = "solution"
INPUT_PATH = os.path.abspath("input.json")
OUTPUT_PATH = os.path.abspath("output.json")
SOL_IN_PATH = os.path.abspath("solutions.json")
SOL_OUT_PATH = os.path.abspath("solutions_output.json")
SCREEN = 2  # 0 for regular, 1 for fullscreen, 2 for small screen
IS_GRAPHIC_ACCEL_ON = True

# genetic tested parameters:
POP_SIZE = 12 # or 100
MUTATION_RATE = 0.1 # 0.015 # 0.005


# genetic constant parameters:
FITTEST_AMOUNT = 10
NUM_GENERATIONS = 3
MUTATION_RATE_MULTIPLIER = 5

# game constant:
NUM_SEGMENTS = 2  # The number of game levels on which we want to learn
START_OF_GAME_MONEY = 500
INIT_WAVE = 1
MAX_EARNINGS_PER_SEGMENT = 1160
WAVES_PER_SEGMENT = 9
GENOME_SIZE = 209
MAX_GENE_INDEX = GENOME_SIZE - 1
BOTTOM_LEFT_CORNER = (0, 2)
TOP_RIGHT_CORNER = (17, 15)
MAX_X = min(abs(TOP_RIGHT_CORNER[0]), 31)
MAX_Y = min(abs(TOP_RIGHT_CORNER[1]), 17)
MIN_X = min(abs(BOTTOM_LEFT_CORNER[0]), 31)
MIN_Y = min(abs(BOTTOM_LEFT_CORNER[1]), 17)

# game tweeks:
EMPTY_GENOME = [Tower() for i in range(209)]
SPEED_MULTIPLIER = 100
DURATION_MULTIPLIER = 1 / SPEED_MULTIPLIER
RANGE_MULTIPLIER = 0.8  # reduce ranged tower range
LEVEL = 2