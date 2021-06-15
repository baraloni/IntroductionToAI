
from GeneticAgent.genetic_resources import TowerType, Tower, TowerLevel
from Pyfense import pyfense

genome1 = [Tower() for i in range(209)]
genome2 = [Tower() for i in range(209)]

for i in range(30):
    if i < 10:
        genome1[i].buy(TowerType.RANGE)
        genome2[i].buy(TowerType.RANGE)
        if i < 7:
            genome1[i].upgrade()
        else:
            genome2[i].upgrade()
            genome2[i].upgrade()

    elif i < 20:
        genome1[i].buy(TowerType.POISON)
        if i < 13:
            genome2[i].buy(TowerType.PLASMA)
    elif i < 27:
        genome2[i].buy(TowerType.RAPID)

genomes = [genome1, genome2]

pyfense.run_sequence_of_genomes(genomes, start_of_game_money=250000)