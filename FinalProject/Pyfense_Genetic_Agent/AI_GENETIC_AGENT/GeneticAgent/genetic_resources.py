import copy
import random
from enum import Enum


class OrderedEnum(Enum):
    """
    Implies an order over the enum's keys by their values.
    """

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class TowerType(Enum):
    """
    Tower Types. Not ordered.
    """
    NO_TOWER = -1
    RAPID = 0
    RANGE = 1
    PLASMA = 2
    POISON = 3
    SLOW = 4


class TowerLevel(OrderedEnum):
    """
    Tower levels. Ordered.
    """
    NO_TOWER = 0
    WEAK = 1
    MEDIUM = 2
    STRONG = 3


# useful dicts and lists:
CHEAP_TOWERS = {TowerType.RAPID, TowerType.RANGE, TowerType.PLASMA}
TOWER_TYPES = [TowerType.NO_TOWER, TowerType.RAPID, TowerType.PLASMA, TowerType.POISON, TowerType.SLOW,
               TowerType.RANGE]
TOWER_LEVELS_NO_NO_TOWER = [TowerLevel.WEAK, TowerLevel.STRONG, TowerLevel.MEDIUM]


class Tower:
    """
    A class that represents a tower.
    A Tower object has a type, a level, and a price, and it can be:
        1. Inquired about the cost of being subjected to a series of actions from {bought, upgraded, downgraded, sold}
        2. Subjected to a series of actions from {bought, upgraded, downgraded, sold}
    """

    REFUND_PERCENTAGE = 0.7

    CHEAP_TOWER_PRICE = 50
    EXPENSIVE_TOWER_PRICE = 80

    def __init__(self):
        """
        Initializes a Tower object.
        """
        self.type = TowerType.NO_TOWER
        self.level = TowerLevel.NO_TOWER
        self.price = 0

    # ############# Get & apply a transformation's price #######################################

    def estimate_update(self, wanted_type, wanted_level):
        """
        Estimates the cost of applying a series of actions upon the tower to get it
        from it's current state to the desired one.
        :param type: TowerType object representing the desired tower type.
        :param level: TowerLevel object representing the desired tower level.
        :return: The estimated price of the update.
        """
        cost = 0
        current_type = self.type
        current_level = self.level

        if current_type != wanted_type:  # sell & buy!
            if current_type != TowerType.NO_TOWER:
                cost -= self.__inquire_sell()
            cost += self.__inquire_buy_new_tower(wanted_type)
            current_type = wanted_type
            current_level = TowerLevel.NO_TOWER if current_type is TowerType.NO_TOWER else TowerLevel.WEAK

        if current_level < wanted_level:  # Upgrade
            cost += self.__inquire_upgrade(current_type, current_level, wanted_level)
        elif current_level > wanted_level:  # Downgrade
            cost += self.__inquire_downgrade(wanted_level)

        return cost

    def update(self, type, level):
        """
        Updating this tower to be of the specified type and level
        :param type: TowerType object representing the desired tower type.
        :param level: TowerLevel object representing the desired tower level.
        :return: The cost of the update.
        """
        cost = 0

        if self.type != type:  # sell & buy!
            if self.type != TowerType.NO_TOWER:
                cost -= self.__sell()
            cost += self.__buy(type)

        if self.level < level:  # Upgrade
            cost += self.__upgrade(level)

        elif self.level > level:  # Downgrade
            cost -= self.__downgrade(level)

        return cost

    # ################ Pricing helpers #####################

    def __inquire_sell(self):
        """
        :return: The amount of money you get back from selling.
        """
        return self.REFUND_PERCENTAGE * self.price

    def __inquire_buy_new_tower(self, type):
        """
        :param type: TowerType object
        :return: The price of buying this type of tower of level == WEAK
        """
        cost = 0

        if not type == TowerType.NO_TOWER:
            cost += self.CHEAP_TOWER_PRICE if type in CHEAP_TOWERS else self.EXPENSIVE_TOWER_PRICE

        return cost

    def __inquire_downgrade(self, wanted_level):
        """
        should only be called when wanting the same tower of lower level.
        :param wanted_level: The wanted level to downgrade to.
        :return: The price of downgrading this tower to the desired level.
        """
        cost = 0

        if self.type != TowerType.NO_TOWER:
            # Sell & buy a weak version:
            cost -= self.__inquire_sell()
            cost += self.__inquire_buy_new_tower(self.type)

            # Upgrade by need:
            if wanted_level != TowerLevel.WEAK:
                cost += self.__inquire_upgrade(self.type, TowerLevel.WEAK, wanted_level)

        return cost

    def __inquire_upgrade(self, curr_type, curr_level, wanted_level):
        """
        :param curr_level: The wanted level to upgrade to.
        :return: The price of upgrading this tower to the given level.
        """
        cost = 0

        if curr_type != TowerType.NO_TOWER:
            if curr_level == TowerLevel.WEAK:
                cost += 80 if curr_type == TowerType.RAPID else 100
            if curr_level < TowerLevel.STRONG and wanted_level == TowerLevel.STRONG:
                cost += 250

        return cost


    # ################## Applying helpers ##################################

    def __sell(self):
        """
        Sells the Tower (sets it to <NO_TOWER, NO_LEVEL>) and returns the amount of money earned.
        """
        refund = 0
        if not self.type == TowerType.NO_TOWER:
            refund += self.price * self.REFUND_PERCENTAGE
            self.type = TowerType.NO_TOWER
            self.level = TowerLevel.NO_TOWER
            self.price = 0
        return refund

    def __buy(self, type):
        """
        Buys the tower (sets it to <type, WEAK>)
        :return cost - the price it took to buy the tower
        :param type: TowerType object
        """
        cost = 0
        if not type == TowerType.NO_TOWER:
            self.type = type
            self.level = TowerLevel.WEAK
            self.price = cost = self.__inquire_buy_new_tower(type)
        return cost


    def __upgrade(self, wanted_level):
        """
        Upgrades the tower to the desired level.
        :param wanted_level: TowerLevel object
        :return cost - the money it cost to upgrade
        """
        cost = 0
        if not self.type == TowerType.NO_TOWER:
            cost = self.__inquire_upgrade(self.type, self.level, wanted_level)
            self.price += cost
            self.level = wanted_level
        return cost

    def __downgrade(self, level):
        """
        Downgrades the tower to the desired level.
        :param level: TowerLevel object
        :return cost - the money we gained from the downgrade
        """
        cost = 0
        type = self.type
        cost += self.__sell()
        cost -= self.__buy(type)
        if self.level < level:
            cost -= self.__upgrade(level)
        return cost

    # ############## Operators ####################

    def __eq__(self, other):
        return self.type, self.level == other.get_tower()

    def __ne__(self, other):
        t, l = other.get_tower()
        return self.type != t or self.level != l

    def __repr__(self):
        if self.type is TowerType.NO_TOWER:
            return "--"
        tower_type = str(self.type.value)
        tower_level = str(self.level.value)
        return tower_type + tower_level

    def __nonzero__(self):
        return self.type != TowerType.NO_TOWER and self.level != TowerLevel.NO_TOWER

        #   ############## Getters ####################

    def get_tower(self):
        return self.type, self.level

    def get_tower_instance(self):
        return self


def get_random_tower():
    """
    generate a random tower. allows for non valid (of NO_TOWER type or level)
    """
    new_tower = Tower()
    type = random.choice(TOWER_TYPES)

    if type == TowerType.NO_TOWER:
        return new_tower

    level = random.choice(TOWER_LEVELS_NO_NO_TOWER)
    new_tower.update(type, level)

    return new_tower

