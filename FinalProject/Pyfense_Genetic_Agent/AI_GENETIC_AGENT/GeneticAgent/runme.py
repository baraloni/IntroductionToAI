import sys
import os
sys.path.append(os.getcwd())

from GeneticAgent.GeneticAlgorithm import GeneticAlgorithm
from GeneticAgent.config import *
from datetime import datetime
from Logger import logger

mode = sys.argv[1]

if mode == "learn":

    log = logger.Logger()
    log.write_run_parameters(POP_SIZE, NUM_GENERATIONS, FITTEST_AMOUNT, MUTATION_RATE,
                                START_OF_GAME_MONEY, NUM_SEGMENTS, WAVES_PER_SEGMENT)

    init_wave = INIT_WAVE

    # ############## Solving the segment  ##############

    fittest_of_all_time = list()
    fittest_of_seg = None

    for seg_idx in range(NUM_SEGMENTS):

        start_time = datetime.now()

        log.create_segment_csv()
        ga = GeneticAlgorithm(init_wave, seg_idx, log, fittest_of_seg)
        fittest_of_seg = ga.run()

        if len(fittest_of_seg) < 2:
            log.write_failure_message(seg_idx)
            log.end_run()
            break

        fittest_of_all_time.append(fittest_of_seg)
        init_wave += WAVES_PER_SEGMENT

        time_elapsed = datetime.now() - start_time
        log.save_segment_execution_time(seg_idx, time_elapsed)

    # ############## Tracing back the segment's solutions ##############

    solutions = dict()

    for seg_idx in range(len(fittest_of_all_time)):
        sol = max(fittest_of_all_time[seg_idx])
        evolution = sol.traceback()
        solutions[seg_idx] = evolution

    log.log_solutions(solutions)

# ############## Present the segment's solutions ##############

if mode == "solution":
    IS_GRAPHIC_ACCEL_ON = False

    # Run them!
    command = ["python3", RUN_FILE, mode, SOL_IN_PATH, SOL_OUT_PATH, str(WAVES_PER_SEGMENT)]
    os.system(" ".join(command))


