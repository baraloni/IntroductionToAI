import os

from GeneticAgent.population import Population
from GeneticAgent.individual import Individual
from GeneticAgent.genetic_resources import *

import numpy as np
import random
import copy
import math
from GeneticAgent.config import *


class GeneticAlgorithm:

    @ staticmethod
    def fitness_function(individual):
        if individual.get_lives() <= 0:  # had died
            return 0

        ancestor_lives = 15 if individual.get_ancestor() is None else individual.get_ancestor().get_lives()

        # Prefers inds that had bad background but succeeded to do risk management [0,1]:
        normalized_lives = 1 - ((ancestor_lives - individual.get_lives()) / 15)

        # [0, inf). 0 means big spender, 1 is very frugal:
        normalized_money = individual.get_money() / individual.get_ancestor().get_money() if \
                           individual.get_ancestor().get_money() != 0 else 1

        if individual.get_lives() < ancestor_lives:  # Survived, barely
            return normalized_lives + normalized_money

        normalized_money_earned = individual.get_money_earned() / MAX_EARNINGS_PER_SEGMENT  # [0,1]

        return normalized_lives + normalized_money + normalized_money_earned  # Survived

    def __init__(self, init_wave, seg, log, pop_seed=None):
        """
        Initializes a Genetic Algorithm object.
        :param init_wave: The starting point in the game from which the algorithm needs to learn.
        :param pop_seed: List of individuals that we be the seed of the initial population.
        """
        self.init_wave = init_wave
        self.num_waves = WAVES_PER_SEGMENT
        self.gen_idx = 0
        self.segment = seg
        self.population = Population(self.segment)
        self.log = log

        if pop_seed is None:
            self.ancestors = [Individual(START_OF_GAME_MONEY, self.segment, genome=[Tower() for i in range(209)])]
            # Build new random population:
            self.population.init_random_pop(START_OF_GAME_MONEY, self.ancestors[0], gen_num=self.gen_idx)
        else:
            self.ancestors = pop_seed
            # Build new population from the individuals in pop_seed:
            self.population.init_pop_from_inds(self.mutation(self.crossover(np.array(pop_seed)), MUTATION_RATE_MULTIPLIER))
            

        # list of np.arrays, where fittest_inds[gen] stores the fittest individuals of that gen:
        self.fittest_inds = list()

    def calculate_pop_fitness(self):
        """
        Updates the population's fitness values.
        """
        self.population.let_live()

        self.population.update()  # update the individual's lifetime achievements (needed for the fitness calc)

        for individual in self.population:
            individual.set_fitness(self.fitness_function(individual))

        self.log_generation()

    def selection(self):
        """
        Selects and stores the FITTEST_AMOUNT fittest individuals.
        :return: The fittest individuals that will create the next generation
        """
        fittest = self.population.fittest_individuals(FITTEST_AMOUNT)
        self.fittest_inds.append(fittest)
        self.log.write_to_run_log("Number of fittest for generation " + str(self.gen_idx) + " is " + str(len(fittest)))
        return fittest

    def cross_parents_genomes(self, p1g, p2g):
        """
        :param p1g: np.array of Tower objects, of size GENOME_SIZE, representing parent1's genome.
        :param p2g: np.array of Tower objects, of size GENOME_SIZE, representing parent2's genome.
        :return: 2 genomes (np.array of Tower objects, of size GENOME_SIZE) that are
                composed of the parents' genomes, and that are valid:
                One of the parent's genome can transform (and afford it) via
                legal actions to the baby's genome
        """
        break_point = random.randint(0, GENOME_SIZE)

        parent_copy_1 = np.split(copy.deepcopy(p1g), [break_point])
        parent_copy_2 = np.split(copy.deepcopy(p2g), [break_point])

        b1g = np.concatenate((parent_copy_1[0], parent_copy_2[1]))
        b2g = np.concatenate((parent_copy_2[0], parent_copy_1[1]))

        return b1g, b2g

    def is_valid_genome(self, baby_genome):
        """
        :param baby_genome: np.array of Tower objects, of size GENOME_SIZE.
        :return: Boolean value representing whether or not there is a legal parent to this baby.
                If There such legal parent:
                    we will return True, the optimal parent and the initial money it passes to it's baby.
                Else:
                    we will return False, None, 0
        """
        money = -math.inf
        opt_ancestor = None

        for ancestor in self.ancestors:
            build_cost = self.evolution_cost(baby_genome, ancestor.get_genome())
            baby_money_after_build = ancestor.get_money() - build_cost
            if baby_money_after_build >= 0 and baby_money_after_build > money:  # legal & optimal parenthood
                money = baby_money_after_build
                opt_ancestor = ancestor

        if money == -math.inf:
            return False, None, 0
        else:
            return True, opt_ancestor, money

    def evolution_cost(self, baby_genome, parent_genome):
        """
        :param baby_genome: np.array of Tower objects, of size GENOME_SIZE, representing the baby's genome
        :param parent_genome: np.array of Tower objects, of size GENOME_SIZE, representing a baby parent's genome.
        :return: The cost of the evolution from parent's genome to baby's genome.
        """
        cost = 0

        for gene in range(GENOME_SIZE):
            if parent_genome[gene] != baby_genome[gene]:
                baby_type, baby_level = baby_genome[gene].get_tower()
                cost += parent_genome[gene].estimate_update(baby_type, baby_level)

        return cost

    def crossover(self, fittest):
        """
        Breeds the fittest individuals until we reach a population of POP_SIZE valid individuals.
        :param fittest: np.array of individuals which we will crossover
        :return: The newly created population.
        """
        new_gen = list()

        while len(new_gen) < POP_SIZE:
            parents_idx = random.sample(range(len(fittest)), 2)
            parent1, parent2 = fittest[parents_idx]
            baby1_genome, baby2_genome = self.cross_parents_genomes(parent1.get_genome(), parent2.get_genome())

            for baby_genome in [baby1_genome, baby2_genome]:
                if len(new_gen) != POP_SIZE:  # We need more babies!
                    is_valid, opt_ancestor, money = self.is_valid_genome(baby_genome)
                    if is_valid:
                        baby = Individual(money, self.segment, genome=baby_genome, ancestor=opt_ancestor, gen_num=parent1.gen_num + 1)
                        baby.set_genetic_parents_ids_string(str(parent1.id) + ", " + str(parent2.id))
                        new_gen.append(baby)

        return new_gen

    @staticmethod
    def mutate_buy_sell_upgrade(baby, mutation_indices):
        # print("baby.money is " + str(baby.money))
        for i in mutation_indices:
            gene = baby.genome[i]
            type = random.choice(list(TowerType))
            level = random.choice(list(TowerLevel))

            baby.change_tower_under_constrains(gene, type, level)

    def mutate(self, baby, mutation_rate_multiplier):
        """
        :param baby: the Individual object it's genome we want to mutate.
        :return: The baby's legally mutated genome.
        """
        mutation_indices = list()
        for gene_idx in range(len(baby.genome)):
            r = random.random()
            if r < (MUTATION_RATE * mutation_rate_multiplier):
                mutation_indices.append(gene_idx)

        # print("mutamutation_indices: " + str(mutation_indices))

        return self.mutate_buy_sell_upgrade(baby, mutation_indices)

    def mutation(self, new_gen, mutation_rate_multiplier=1):
        """
        Mutates the population's genome.
        :param new_gen: A new generation of POP_SIZE valid individuals.
        :return: POP_SIZE valid individuals after mutation, from new_gen.
        """
        for baby in new_gen:
            self.mutate(baby, mutation_rate_multiplier)
        return new_gen


    def log_generation(self):
        """
        log the following:
            generation
            id
            fitness
            lives lost
            earned money
            spent money
            waves survived
        """
        data = list()
        average_fitness = 0
        max_fitness = 0
        
        for i in self.population:
            average_fitness += i.get_fitness()
            max_fitness = max(max_fitness, i.get_fitness())
            lives_lost = i.get_ancestor().get_lives() - i.get_lives()
            # ["Generation, ID, Fitness, Lives lost, Money earned, Money spent, Waves Survived"]
            d = [self.gen_idx, i.id, i.get_fitness(), lives_lost, i.get_money_earned(), i.get_money_spent(), i.get_wave()]
            data.append([str(s) for s in d])

        self.log.save_generation_summary(self.gen_idx, average_fitness / len(self.population), max_fitness)
        self.log.save_generation_data(data)


    def run(self):
        """
        :return: A list of the fittest individual from every generation along the history
        """
        self.calculate_pop_fitness()
        
        while self.gen_idx < NUM_GENERATIONS - 1:

            # Create new generation:
            fittest = self.selection()

            if len(fittest) >= 2:
                potential_gen = self.crossover(fittest)

            else:
                return []

            new_gen = self.mutation(potential_gen)

            self.gen_idx += 1

            # Set new generation to be the new population, and let them live!
            self.population.replace_generation(new_gen)
            self.calculate_pop_fitness()

        return self.fittest_inds[-1]

