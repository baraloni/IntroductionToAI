import os
import json

from GeneticAgent.individual import Individual
from GeneticAgent.config import *
import numpy as np

FIRST_GENERATION_IN_SEGMENT = 0


class PopulationIterator:
    """
    Iterates over the Individuals in the Population (in order of creation).
    """
    def __init__(self, population):
        self.__population = population
        self.__index = 0

    def __next__(self):
        if self.__index < (len(self.__population)):
            res = self.__population.individuals[self.__index]
            self.__index += 1
            return res
        # End of Iteration
        raise StopIteration


class Population:

    def __init__(self, seg):
        """
        Initialize a blank Population
        """
        self.segment = seg
        self.individuals = list()
        self.fittest = list()
        self.gen_num = 0

    def init_random_pop(self, money, ancestor, gen_num=0):
        """
         Initialized a random population.
         :param init_wave: The individual's era.
         :param money: The individual's funds to use in it's lifetime.
         """
        for i in range(POP_SIZE):
            self.individuals.append(Individual(money, self.segment, gen_num=gen_num, ancestor=ancestor))

    def init_pop_from_inds(self, individuals):
        """
        Initializes a population from
        :param individuals: list of Individual objects to compose the population
        """
        self.individuals = individuals
        for individual in individuals:
            individual.set_generation(FIRST_GENERATION_IN_SEGMENT)

    def let_live(self):
        """
        Lets the individuals in the population live their life.
        The individuals get updated in their lifetime.
        """
        # create & write to INPUT_PATH file:
        genomes = dict()
        for individual in self.individuals:
            genomes[individual.get_id()] = [individual.encode_genome_to_string(), individual.get_lives()]

        with open(INPUT_PATH, 'w') as f:
            json.dump(genomes, f)

        # run the program!
        command = ["python3", RUN_FILE, "learn", INPUT_PATH, OUTPUT_PATH, str(self.segment * WAVES_PER_SEGMENT + 1),
                   str(WAVES_PER_SEGMENT), str(self.gen_num)]
        os.system(" ".join(command))

    def update(self):
        with open(OUTPUT_PATH) as f:
            achievements = json.load(f)

            for individual in self.individuals:
                individual.update(achievements[str(individual.get_id())])

    def fittest_individuals(self, ind_amount):
        """
        :param ind_amount: The amount of fittest individuals to be returned.
        :return: The ind_amount fittest individuals (not sorted)
        """
        def filterIndividuals(individual):
            if individual.get_fitness() > 0:
                return True
            else:
                return False

        live_individuals = np.array(list(filter(filterIndividuals, self.individuals)))

        if len(live_individuals) - ind_amount > 0:  # There are more then ind_amount live_individuals, can sort!
            ordered_idx = np.argpartition(live_individuals, len(live_individuals) - ind_amount)
            return live_individuals[ordered_idx[len(live_individuals) - ind_amount:]]

        else:
            return live_individuals  # Not enough live ones.. return what we've got

    def replace_generation(self, new_gen):
        """
        Update the population to be consisted solely from the new generation.
        :param new_gen: list of individuals that compose the new generation of the population
        """
        self.individuals = new_gen
        self.fittest.clear()
        self.gen_num += 1

    # ###################### operators ######################

    def __iter__(self):
        return PopulationIterator(self)

    def __len__(self):
        return len(self.individuals)