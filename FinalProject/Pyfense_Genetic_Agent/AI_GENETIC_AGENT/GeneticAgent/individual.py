import random as rand
from GeneticAgent.genetic_resources import *
from GeneticAgent.config import *
import numpy as np


class Individual:
    current_id = 0
    current_gen = -1

    def __init__(self, ancestor_money, seg, genome=None, ancestor=None, gen_num=0):
        """
        Initialize an Individual Object.
        :param genome: the individual's genome: array of Tower objects of size genome_size.
        :param ancestor: An Individual object from which we can get this object
                      (transformation suffice the constraint of the ancestor's money)
        """
        prev_gen = Individual.current_gen

        if Individual.current_gen != gen_num:
            Individual.current_id = 0
            gen_num = gen_num % NUM_GENERATIONS
            Individual.current_gen = gen_num

        self.segment = seg
        self.id = Individual.current_id  % POP_SIZE
        Individual.current_id += 1

        self.ancestor = ancestor
        self.money = ancestor_money

        self.gen_num = gen_num
        self.genetic_parents_ids_string = None

        if prev_gen == -1:
            self.gen_num = -1
            Individual.current_id = 0

        if genome is None:
            self.randomize_genome()
        else:
            self.genome = genome

        self.fitness = 0
        self.lives = 15 if ancestor is None else ancestor.get_lives()
        self.wave = None
        self.money_earned = None
        self.money_spent = None

    # ##################### Functionality #####################

    def change_tower_under_constrains(self, tower, tower_type, level):
        current_type = tower_type
        current_level = TowerLevel.NO_TOWER.value

        while current_level < level.value:
            # Try upgrade..
            current_level += 1
            cost = tower.estimate_update(current_type, TowerLevel(current_level))

            if cost > self.money:  # Too pricey. Settle for last option
                current_level -= 1
                break

            elif level is current_level:  # I want (and can afford) this tower!
                break

        if current_level == TowerLevel.NO_TOWER.value:
            current_type = TowerType.NO_TOWER
            # print("no mutation", tower_type, level)

        cost = tower.update(current_type, TowerLevel(current_level))
        self.pay(cost)

    def buy_random_towers(self):
        """
        :return: A list of Random Tower objects that can be bought with self.init_money.
        """
        max_towers = self.money // Tower.CHEAP_TOWER_PRICE
        num_towers = rand.randint(0, max_towers)

        towers_to_place = list()
        for i in range(num_towers):
            if self.money < Tower.CHEAP_TOWER_PRICE:  # Can't afford a new tower
                break

            new_tower = Tower()
            type = rand.choice(TOWER_TYPES)
            level = rand.choice(TOWER_LEVELS_NO_NO_TOWER)

            if type is TowerType.NO_TOWER:  # Don't wast your time
                continue

            self.change_tower_under_constrains(new_tower, type, level)

            if new_tower:  # if new_tower is not of type NO_TOWER
                towers_to_place.append(new_tower)

        return towers_to_place

    def randomize_genome(self):
        """
        Assign self.genome with a newly randomized genome (that suffice the constraint of self.init_money)
        """
        # Buy Towers Randomly:
        towers_to_place = self.buy_random_towers()

        # Place towers randomly:
        placements = rand.sample(range(GENOME_SIZE), len(towers_to_place))
        self.genome = np.array(EMPTY_GENOME)
        self.genome[placements] = towers_to_place

    def traceback(self):
        """
        :return: A list of this individual's ancestry (from it's single parent), until the very first
                randomized object.
        """
        evolution = list()
        curr = self
        while curr.get_generation() > -1:
            curr_genome_str = curr.encode_genome_to_string()
            evolution.append(curr_genome_str)
            curr = curr.get_ancestor()

        return evolution[::-1]

    def take_refund(self, refund):
        """
        Adds refund to self.money.
        :param refund: double
        """
        self.money += refund

    def pay(self, cost):
        """
        Deducts cost from self.money
        :param cost: double
        """
        self.money -= cost

    def encode_genome_to_string(self):
        string_genome = str()
        for i in range(GENOME_SIZE):
            string_genome += self.genome[i].__str__() + ' '

        return string_genome[:-1]  # remove last ' '

    # ################ operators #################

    # TODO: maybe we don't need all of them:)

    def __eq__(self, other):
        """
        :param other: an Individual object
        :return: True iff the 2 Individuals share the same fitness value.
        """
        if not isinstance(other, Individual):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.fitness == other.fitness

    def __lt__(self, other):
        """
        :param other: an Individual object
        :return: True iff this object has a smaller fitness value than other's.
        """
        if not isinstance(other, Individual):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.fitness < other.fitness

    def __gt__(self, other):
        """
        :param other: an Individual object
        :return: True iff this object has a bigger fitness value than other's.
        """
        if not isinstance(other, Individual):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.fitness > other.fitness

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        name = str(self.segment) + ", " + str(self.gen_num) + ", " + str(self.id)
        ind_line = "Individual (" + name + "), fit: " + str(self.fitness) + "\n"
        parents = "No parents" if self.genetic_parents_ids_string is None else self.genetic_parents_ids_string
        parents_line = "Genetic parents' ids: " + parents + "\n"
        ancestor = "No ancestor" if self.ancestor is None else str(self.ancestor.id)
        ancestor_line = "Chosen ancestor id: " + ancestor + "\n"
        genome = "Genome is: " + self.encode_genome_to_string()
        return ind_line + parents_line + ancestor_line + genome

    # ################# setters #################

    def set_fitness(self, fitness_value):
        self.fitness = fitness_value

    def set_money(self, money):
        self.money = money

    def update(self, achievement):
        self.wave = int(achievement[0])
        self.lives = int(achievement[1])
        self.money_spent = int(achievement[2])
        self.money_earned = int(achievement[3])
        self.money += self.money_earned

    def set_generation(self, gen):
        self.gen_num = gen

    def set_genetic_parents_ids_string(self, id_string):
        self.genetic_parents_ids_string = id_string

    # ################# getters #################

    def get_id(self):
        return self.id

    def get_genome(self):
        return self.genome

    def get_fitness(self):
        return self.fitness

    def get_money(self):
        return self.money

    def get_wave(self):
        return self.wave

    def get_lives(self):
        return self.lives

    def get_money_spent(self):
        return self.money_spent

    def get_money_earned(self):
        return self.money_earned

    def get_ancestor(self):
        return self.ancestor

    def get_genetic_parents_ids(self):
        return self.genetic_parents_ids_string

    def get_generation(self):
        return self.gen_num