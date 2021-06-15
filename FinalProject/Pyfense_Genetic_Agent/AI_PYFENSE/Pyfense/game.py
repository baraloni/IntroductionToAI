"""
PyFenseGame -  Top Level Scene during the game, onto which all the other
Layers get added.Responsible for dynamic pathfinding and communication between
user interaction through the HUD and entities like towers.
"""
import sys

from cocos.director import director
from cocos import scene
from cocos import actions

from Pyfense.genetic_resources import Tower, TowerType
from Pyfense import map
from Pyfense import entities
from Pyfense import hud
from Pyfense.highscore import PyFenseLost
from Pyfense import tower
from Pyfense import resources
from Pyfense import highscore
from Pyfense.resources import MIN_X, MAX_X, MIN_Y, MAX_Y, MAX_GENE_INDEX, START_OF_GAME_MONEY
import copy



class PyFenseGame(scene.Scene):

    def __init__(self, genomes, waves_per_segment, currentLives=15, money_after_build=START_OF_GAME_MONEY, init_wave=0,
                 gen_num=0):
        super().__init__()
        self.is_display_genome_mode_on = (gen_num < 0)
        # initialise game grid to store where enemies can walk,
        # towers can be build and where towers are already built
        # one grid cell is 60x60px large (full hd resolution scale)
        # gameGrid can be called by using gameGrid[y][x]
        # key:
        # 0 := no tower can be build, no enemy can walk
        # 1 := no tower can be build, enemy can walk
        # 2 := helper for pathfinding,replaced with 1 after path was found
        # 3 := tower can be build, no enemy can walk
        # 4 := tower has been built, no enemy can walk,
        # no tower can be build (can upgrade (?))
        # 100-200 := 1 + towerNr + towerLvl has been built here
        self.gameGrid = [[0 for x in range(32)] for x in range(18)]
        self.gameGrid, \
        self.startTile, \
        self.endTile = resources.initGrid(resources.LEVEL)

        resources.load_waves()
        resources.load_entities()

        self.movePath = self._load_path()
        self.levelMapName = "lvl" + str(resources.LEVEL)
        self._load_map()
        self._display_entities()
        self._display_hud()

        # shahar/
        self.hud.update_gen_number(gen_num)
        self.hud.update_live_number(currentLives)
        self.waves_per_genome = waves_per_segment
        self.currentWave = init_wave
        self.max_no_of_waves = init_wave + waves_per_segment * len(genomes)
        self.money = money_after_build
        self.money_after_build = money_after_build
        self.total_earned = 0
        self.total_spent = 0
        self.genomes = genomes
        self.curr_genome_num = 0
        self.currentLives = currentLives

        # /shahar

        highscore.currentWave = self.currentWave
        director.interpreter_locals["game"] = self

        try:
            test = sys.argv[1]
        except:
            test = "notest"

        if test == "test":
            self.currentLives = 200
            self.money = 10000

    def _load_path(self):
        """
        Dynamically finds the path for the enemies, by going through the
        gameGrid Matrix. Contains both the path for enemies and their health-
        bars, enemies rotate additionally to moving.
        """
        currentTile = copy.deepcopy(self.startTile)
        # move[0] for enemy with rotation and move[1] for healthbar
        move = [[], []]
        pos = self._get_pixel_coords_from_position(self.startTile)

        while (currentTile[0] != self.endTile[0] or
               currentTile[1] != self.endTile[1]):

            # Right
            if (self.gameGrid[currentTile[0]][currentTile[1] + 1] == 2):
                # Rotate right
                move[0].append(actions.RotateTo(0, 0))
                # move[1].append([])
                # Move right
                for j in range(1, 11):
                    move[0].append((pos[0] + 6 * j, pos[1]))
                    # move[1].append((6, 0))
                # Next position
                pos = (pos[0] + 60, pos[1])
                currentTile[1] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            # Up
            elif (self.gameGrid[currentTile[0] + 1][currentTile[1]] == 2):
                # Rotate up
                move[0].append(actions.RotateTo(270, 0))
                # move[1].append([])
                # Move up
                for j in range(1, 11):
                    move[0].append((pos[0], pos[1] + 6 * j))
                    move[1].append((0, 6))
                # Next position
                pos = (pos[0], pos[1] + 60)
                currentTile[0] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            # Down
            elif (self.gameGrid[currentTile[0] - 1][currentTile[1]] == 2):
                # Rotate down
                move[0].append(actions.RotateTo(90, 0))
                # move[1].append([])
                # Move down
                for j in range(1, 11):
                    move[0].append((pos[0], pos[1] - 6 * j))
                    # move[1].append((0, -6))
                # Next position
                pos = (pos[0], pos[1] - 60)
                currentTile[0] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1
            # Left
            elif (self.gameGrid[currentTile[0]][currentTile[1] - 1] == 2):
                # Rotate left
                move[0].append(actions.RotateTo(180, 0))  # RotateLeft
                # move[1].append([])  # placeholder
                # Move left
                for j in range(1, 11):
                    move[0].append((pos[0] - 6 * j, pos[1]))
                    # move[1].append((-6, 0))
                # Next position
                pos = (pos[0] - 60, pos[1])
                currentTile[1] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            else:
                break
        self.gameGrid[self.startTile[0]][self.startTile[1]] = 1
        return move

    def _load_map(self):
        self.levelMap = map.PyFenseMap(self.levelMapName)
        self.add(self.levelMap, z=0)

    def _display_entities(self):
        startTile = self._get_pixel_coords_from_position(self.startTile)
        endTile = self._get_pixel_coords_from_position(self.endTile)
        self.entityMap = entities.PyFenseEntities(self.movePath,
                                                  startTile, endTile, self.is_display_genome_mode_on)
        self.entityMap.push_handlers(self)
        self.add(self.entityMap, z=1)

    def _display_hud(self):
        self.hud = hud.PyFenseHud()
        self.hud.push_handlers(self)
        self.add(self.hud, z=2)

    def _set_grid_pix(self, x, y, kind):
        """
        Set the gameGrid (int) to a certain Value at a certain point,
        specified by the coordinates in Pixel
        """
        if kind < 0 or kind > 200:
            print("WRONG GRID TYPE, fix ur shit")
            return
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self._set_grid(grid_x, grid_y, kind)

    def _set_grid(self, grid_x, grid_y, kind):
        """
        Set the gameGrid (int) to a certain value at a certain point,
        specified by the cell
        """
        if kind < 0 or kind > 200:
            print("WRONG GRID TYPE, fix ur shit")
            return
        self.gameGrid[grid_y][grid_x] = kind

    def _get_tile_value_from_pixel_coords(self, x, y):
        """
        Returns the value of the gameGrid (int) at the specified pixel
        coordinates
        """
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        # gracefully fail for resolution edge cases
        if grid_x > 31:
            grid_x = 31
        if grid_y > 17:
            grid_y = 17
        return self.gameGrid[grid_y][grid_x]

    def _get_pixel_coords_from_position(self, grid):
        """Returns a tupel of the cell number when providing a
        coordinate tupel
        """
        x_grid = grid[1]
        y_grid = grid[0]
        x = 30 + x_grid * 60
        y = 30 + y_grid * 60
        return (x, y)

    def on_enemy_death(self, enemy):
        """Credits the enemy's worth in money to the player"""
        worth = enemy.attributes["worth"]
        self.money += worth
        self.total_earned += worth
        self.hud.update_currency_number(self.money)

    def on_user_mouse_motion(self, x, y):
        self.hud.currentCellStatus = self._get_tile_value_from_pixel_coords(x, y)

    def on_build_tower(self, towerNumber, pos_x, pos_y):
        """
        expects positions in pixel value
        """
        if self._get_tile_value_from_pixel_coords(pos_x, pos_y) > 3:
            return 0# shahar
        toBuildTower = tower.PyFenseTower(towerNumber, (pos_x, pos_y))
        if toBuildTower.attributes["cost"] > self.money:
            return 0# shahar
        #self.currentCurrency -= self.entityMap.build_tower(toBuildTower)
        # shahar/
        cost = self.entityMap.build_tower(toBuildTower)
        self.money -= cost
        self.total_spent += cost
        # /shahar

        self.hud.update_currency_number(self.money)
        self._set_grid_pix(
            pos_x, pos_y, int(float("1" + str(towerNumber) +
                                    str(toBuildTower.attributes["lvl"]))))

        return 1 # shahar

    def on_upgrade_tower(self, position):
        """
        expects position as (x_pixel, y_pixel)
        Updates the the tower at the given position with a new tower with
        upgraded attributes and assets. Also updates the change in the
        Map-Matrix
        """
        oldTower = self.entityMap.get_tower_at(position)
        towerLevel = oldTower.attributes["lvl"]
        if towerLevel == 3:
            return
        towerNumber = oldTower.attributes["tower"]
        cost = resources.tower[towerNumber][towerLevel + 1]["cost"]
        if cost > self.money:
            return
        self.total_spent += cost # shahar
        self.money -= cost
        self.hud.update_currency_number(self.money)
        self.entityMap.remove_tower(position)
        newTower = tower.PyFenseTower(
            towerNumber, position, towerLevel + 1)
        self.entityMap.build_tower(newTower)
        (x, y) = position
        self._set_grid_pix(x, y, int(float("1" + str(towerNumber) +
                                           str(towerLevel + 1))))

    def on_destroy_tower(self, position):
        """
        expexts position in pixels and in format (x, y)
        Returns 70% of the Money invested in the Tower when destroying it
        """
        (x, y) = position
        self._set_grid_pix(x, y, 3)
        #self.currentCurrency += 0.7 * self.entityMap.remove_tower(position)
        # /shahar
        cost = 0.7 * self.entityMap.remove_tower(position)
        self.money += cost
        self.total_earned += cost
        # /shahar

        self.hud.update_currency_number(self.money)

    def on_next_wave(self):
        self.hud.start_next_wave_timer()

    def on_next_wave_timer_finished(self):
        """
        Starts to add the next wave to the Screen and updates the display
        """
        self.currentWave += 1

        # shahar/
        if self.currentWave > self.max_no_of_waves:
            director.replace(PyFenseLost(self.currentWave, self.currentLives, self.total_earned, self.total_spent))

        elif not (self.currentWave - 1) % self.waves_per_genome:
            self.load_next_genome_to_grid()

        # /shahar
        self.entityMap.next_wave(self.currentWave)
        self.hud.update_wave_number(self.currentWave)
        highscore.currentWave = self.currentWave

    def on_enemy_reached_goal(self):
        """
        Gets called everytime an enemy reached the final cell. Transistion
        to the GameOver Screen when the game is finished.
        """
        self.currentLives -= 1
        self.hud.update_live_number(self.currentLives)
        if self.currentLives == 0:
            director.replace(PyFenseLost(self.currentWave, self.currentLives, self.total_earned, self.total_spent))

    def load_next_genome_to_grid(self):
        current_genome = self.genomes[self.curr_genome_num]

        gene_index = 0

        # this is to enable us to spend more money then we have during changes:
        self.money += 250000  # i'll reduce currentCurrency the by 250000 after changes are made

        for x_index in range(MIN_X, MAX_X + 1):
            if gene_index > MAX_GENE_INDEX:
                break

            for y_index in range(MIN_Y, MAX_Y + 1):
                if gene_index > MAX_GENE_INDEX:
                    break

                curr_tile = self.gameGrid[y_index][x_index]

                if curr_tile < 3:
                    continue

                if current_genome[gene_index].type != TowerType.NO_TOWER:
                    curr_tile_kind = max(int((curr_tile - 100) / 10), -1)
                    curr_tile_level = max(int(curr_tile - 100 - curr_tile_kind*10), 1)

                    wanted_type = current_genome[gene_index].type.value
                    wanted_level = current_genome[gene_index].level.value

                    x_pixel, y_pixel = self._get_pixel_coords_from_position((y_index, x_index))

                    if curr_tile_kind != wanted_type or (curr_tile_level > wanted_level):
                        if curr_tile > 5:
                            self.on_destroy_tower((x_pixel, y_pixel))

                        self.on_build_tower(wanted_type, x_pixel, y_pixel)
                        curr_tile_level = 1


                    num_upgrades = wanted_level - curr_tile_level

                    while num_upgrades > 0:
                        self.on_upgrade_tower((x_pixel, y_pixel))
                        num_upgrades -= 1

                gene_index += 1

        self.money -= 250000

        if len(self.genomes) == 1:  # if we're running a single game, reset to money_after_build (do not validate)
            self.money = self.money_after_build

        assert(self.money >= 0)
        self.hud.update_currency_number(self.money)
        self.curr_genome_num += 1
        # print("curr currency: " + str(self.currentCurrency))

    def cell_state_at_position(self, position):
        """
        # 0 := no tower can be build, no enemy can walk
        # 1 := no tower can be build, enemy can walk
        # 2 := helper for pathfinding,replaced with 1 after path was found
        # 3 := tower can be build, no enemy can walk
        # 4 := tower has been built, no enemy can walk,
        # no tower can be build (can upgrade (?))
        # 100-200 := 1 + towerNr + towerLvl has been built here
        """
        return self.gameGrid[position[1]][position[0]]

    def tower_number_at_position(self, position):
        # -1 := no tower
        # 0-4 := tower number
        state = self.gameGrid[position[1]][position[0]]
        if state > 3:
            return (state - 100) / 10
        return -1

    def tower_level_at_position(self, position):
        # -1 := no tower
        # 1-3 := tower level
        state = self.gameGrid[position[1]][position[0]]
        if state > 3:
            return state - ((state / 10) * 10)
        return -1

    def cell_options(self, position):
        """
        returns a list of the possible actions for the cell in given position.
        possible list items are:
        0 - sell
        1y1 - build tower y
        1y2/3 - upgrade tower y to level 2/3
        """
        possible_actions = []
        tower_level = self.tower_level_at_position(position)
        if tower_level >= 0:  # if tower already built
            possible_actions.append(0)
            if tower_level == 3:  # if tower is at highest level
                return possible_actions
            tower_number = self.tower_number_at_position(position)
            cost = resources.tower[tower_number][tower_level + 1]["cost"]
            if cost > self.money:  # if cost too high
                return possible_actions
            else:
                return possible_actions.append(tower_level + 101 + tower_number*10)
        else:
            for i in range(5):
                possible_tower = tower.PyFenseTower(i, position)
                if possible_tower.attributes["cost"] <= self.money:
                    possible_actions.append(i+101)
            return possible_actions

    def get_wave_num(self):
        return self.currentWave

    def get_game_grid(self):
        """
        32X18 list of lists of ints
        """
        return self.gameGrid

    def get_current_currency(self):
        return self.money

    def distance_of_position_from_start_square(self, position):
        return resources.distance(self.startTile, position)
