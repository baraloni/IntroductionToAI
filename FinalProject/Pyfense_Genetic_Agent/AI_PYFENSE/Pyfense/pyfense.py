"""
Mainfile, draws Menu including Level Select, Highscore, Options and About page.
Reads settings from /data/settings.txt. Level Select starts game with
selected level from game.
"""

import pyglet
from pyglet.window import key
from pyglet import font

from gc import collect
import numpy as np

import cocos
import cocos.menu
from cocos.director import director
from cocos.layer import ColorLayer, MultiplexLayer
from cocos import text

import os  # for loading custom image
import sys
import json

# THIS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))), "AI_PYFENSE")
THIS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))), "Pyfense_Genetic_Agent", "AI_PYFENSE")
sys.path.append(os.path.abspath(THIS_FILE))

from Pyfense import modmenu
from Pyfense import game
from Pyfense import mapBuilder
from Pyfense import highscore
from Pyfense import resources
from Pyfense.genetic_resources import Tower, TowerType, TowerLevel

font.add_directory(os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), 'assets'))
_font_ = 'Orbitron Light'


class MainMenu(cocos.menu.Menu):

    def __init__(self, scene):
        super().__init__('')
        self.font_title['font_name'] = _font_
        self.font_title['font_size'] = 72

        self.font_item['font_name'] = _font_
        self.font_item['font_size'] = 35

        self.font_item_selected['font_name'] = _font_
        self.font_item_selected['font_size'] = 41

        self.menu_anchor_x = cocos.menu.CENTER
        self.menu_anchor_y = cocos.menu.CENTER

        self.scene = scene

        self.logo = cocos.sprite.Sprite(resources.logo)
        self.w, self.h = director.get_window_size()
        self.logo.position = (self.w / 2 + 20, self.h - 175)
        self.logo.scale = 0.5
        self.scene.add(self.logo, z=1)
        director.interpreter_locals["pyfense_main"] = self

        items = []
        items.append(cocos.menu.MenuItem('Start Game', self.on_level_select))
        items.append(cocos.menu.MenuItem('Scores', self.on_scores))
        items.append(cocos.menu.MenuItem('Settings', self.on_settings))
        items.append(cocos.menu.MenuItem('Help', self.on_help))
        items.append(cocos.menu.MenuItem('About', self.on_about))
        items.append(cocos.menu.MenuItem('Exit', self.on_quit))
        self.create_menu(items)
        self.schedule(self._scale_logo_main_menu)

    def on_level_select(self):
        self._scale_logo_sub_menu()
        self.parent.switch_to(1)

    def on_settings(self):
        self._scale_logo_sub_menu()
        self.parent.switch_to(2)

    def on_scores(self):
        self._scale_logo_sub_menu()
        self.parent.switch_to(3)

    def on_help(self):
        self._scale_logo_sub_menu()
        self.parent.switch_to(4)

    def on_about(self):
        self._scale_logo_sub_menu()
        self.parent.switch_to(5)

    def on_quit(self):
        pyglet.app.exit()

    def _scale_logo_main_menu(self, dt):
        if self.parent.enabled_layer == 0:
            self.logo.position = (self.w / 2 + 20, self.h - 175)
            self.logo.scale = 0.5

    def _scale_logo_sub_menu(self):
        self.logo.position = (self.w / 2 + 20, self.h - 90)
        self.logo.scale = 0.25


# class LevelSelectLayer(Layer):
#     is_event_handler = True

#     def __init__(self):
#         super().__init__()

#     def on_enter(self):
#         super().on_enter()
#         self.parent.switch_to(3)
#         director.push(LevelSelectMenu())

# class LevelSelectScene(Scene):

#     def __init__(self):
#         super().__init__()
#         self.add(LevelSelectLayer(), z=1)


class LevelSelectMenu(cocos.menu.Menu):

    def __init__(self):
        super().__init__(' ')
        self.items = None
        self.initialise()

    def initialise(self):
        self.font_title['font_name'] = _font_
        self.font_title['font_size'] = 72

        self.font_item['font_name'] = _font_
        self.font_item['font_size'] = 35

        self.font_item_selected['font_name'] = _font_
        self.font_item_selected['font_size'] = 41

        self.menu_anchor_x = cocos.menu.CENTER
        self.menu_anchor_y = cocos.menu.CENTER

        self.items = []
        image_lvl1 = resources.background["lvl1"]
        lvl1 = modmenu.ImageMenuItem(image_lvl1,
                                     lambda: self.on_start(1))
        Back = cocos.menu.MenuItem('Back', self.on_quit)
        Back.y -= 30

        image_lvl2 = resources.background["lvl2"]
        lvl2 = modmenu.ImageMenuItem(image_lvl2,
                                     lambda: self.on_start(2))
        mapBuilderActivated = "nobuilder"
        try:
            mapBuilderActivated = sys.argv[1]
        except:
            mapBuilderActivated = "nobuilder"

        if (mapBuilderActivated == "builder"):
            MapBuilder = cocos.menu.MenuItem('MapBuilder', self.on_mapBuilder)
            MapBuilder.y -= 20

        if (
                os.path.isfile(os.path.join(
                    os.path.dirname(
                        os.path.abspath(__file__)), "assets/lvlcustom.png"))):
            customImage = resources.load_custom_image()
            lvl1.scale = 0.18
            lvl1.y = 30
            self.items.append(lvl1)
            lvl2.scale = 0.18
            lvl2.y -= 150
            self.items.append(lvl2)
            customItem = (
                modmenu.ImageMenuItem(
                    customImage, lambda: self.on_start("custom")))
            customItem.scale = 0.22
            customItem.y -= 300
            self.items.append(customItem)
            if (mapBuilderActivated == "builder"):
                MapBuilder.y -= 340
                Back.y -= 20
            Back.y -= 320
        # custom map has to be positioned correctly in Menu
        else:
            lvl1.scale = 0.28
            lvl1.y = 0
            self.items.append(lvl1)
            lvl2.scale = 0.28
            lvl2.y -= 300
            self.items.append(lvl2)
            if (mapBuilderActivated == "builder"):
                MapBuilder.y -= 320
                Back.y -= 20
            Back.y -= 300
        if (mapBuilderActivated == "builder"):
            self.items.append(MapBuilder)

        self.items.append(Back)
        width, height = director.get_window_size()
        self.create_menu(self.items)

    def on_start(self, lvl):
        """
        Starts the game with the selected level "lvl"
        """
        self.parent.switch_to(3)
        director.push(game.PyFenseGame(lvl))

    def on_mapBuilder(self):
        """
        Starts the Mapbuilder
        """
        director.push(mapBuilder.PyFenseMapBuilder())

    def on_quit(self):
        self.parent.switch_to(0)


class ScoresLayer(ColorLayer):
    is_event_handler = True
    fontsize = 40

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h - 86)

        self.table = None

    def on_enter(self):
        super().on_enter()
        score = highscore.get_score()
        if self.table:
            self._remove_old()
        self.table = []
        self.font_top = {}
        self.font_top['font_size'] = self.fontsize
        self.font_top['bold'] = True
        self.font_top['font_name'] = _font_
        self.font_label = {}
        self.font_label['font_size'] = self.fontsize
        self.font_label['bold'] = False
        self.font_label['font_name'] = _font_
        Head_Pos = text.Label('',
                              anchor_x='right',
                              anchor_y='top',
                              **self.font_top)
        Head_Name = text.Label('Name',
                               anchor_x='left',
                               anchor_y='top',
                               **self.font_top)
        Head_Wave = text.Label('Wave',
                               anchor_x='right',
                               anchor_y='top',
                               **self.font_top)
        self.table.append((Head_Pos, Head_Name, Head_Wave))
        self.table.append((text.Label(''), text.Label(''), text.Label('')))
        for i, entry in enumerate(score):
            pos = text.Label('%i.    ' % (i + 1),
                             anchor_x='right',
                             anchor_y='top',
                             **self.font_label)
            try:
                name = text.Label(entry[1].strip(),
                                  anchor_x='left',
                                  anchor_y='top',
                                  **self.font_label)
            except IndexError:
                print("highscore file broken")
                name = text.Label("Error",
                                  anchor_x='left',
                                  anchor_y='top',
                                  **self.font_label)
            wave = text.Label(entry[0],
                              anchor_x='right',
                              anchor_y='top',
                              **self.font_label)
            self.table.append((pos, name, wave))
        self._process_table()

    def _remove_old(self):
        for item in self.table:
            pos, name, wave = item
            self.remove(pos)
            self.remove(name)
            self.remove(wave)
        self.table = None

    def _process_table(self):
        w, h = director.get_window_size()
        for i, item in enumerate(self.table):
            pos, name, wave = item
            pos_y = h - 200 - (self.fontsize + 15) * i
            pos.position = (w / 2 - 330., pos_y)
            name.position = (w / 2 - 300., pos_y)
            wave.position = (w / 2 + 350., pos_y)
            self.add(pos, z=2)
            self.add(name, z=2)
            self.add(wave, z=2)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True


class OptionsMenu(cocos.menu.Menu):

    def __init__(self):
        super().__init__(' ')

        self.font_title['font_name'] = _font_
        self.font_title['font_size'] = 72

        self.font_item['font_name'] = _font_
        self.font_item['font_size'] = 35

        self.font_item_selected['font_name'] = _font_
        self.font_item_selected['font_size'] = 41

        self.menu_anchor_x = cocos.menu.CENTER
        self.menu_anchor_y = cocos.menu.CENTER
        items = []
        items.append(
            cocos.menu.ToggleMenuItem(
                'Show FPS: ', self.on_show_fps,
                resources.settings["general"]["showFps"]))
        items.append(
            cocos.menu.ToggleMenuItem('Fullscreen: ',
                                      self.on_fullscreen, False))
        items.append(
            cocos.menu.ToggleMenuItem('Vsync: ', self.on_vsync,
                                      resources.settings["window"]["vsync"]))
        items.append(
            cocos.menu.ToggleMenuItem('Sounds: ', self.on_sounds,
                                      resources.settings["general"]["sounds"]))
        items.append(
            cocos.menu.MenuItem('Back', self.on_quit))
        self.create_menu(items)

    def on_show_fps(self, value):
        director.show_FPS = value

    def on_fullscreen(self, value):
        director.window.set_fullscreen(value)

    def on_vsync(self, value):
        director.window.set_vsync(value)

    def on_sounds(self, value):
        resources.sounds = not resources.sounds
        if (resources.music_player.playing):
            resources.music_player.pause()
        else:
            resources.music_player.play()

    def on_quit(self):
        self.parent.switch_to(0)


class HelpLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h - 86)

    def on_enter(self):
        super().on_enter()
        w, h = director.get_window_size()
        nr_towers = len(resources.tower)
        help_text = text.Label('Press Q to quit the running level or Esc '
                               'to enter the Pause Menu',
                               font_name=_font_,
                               font_size=20,
                               anchor_x='center',
                               anchor_y='center')
        help_text.element.width = w * 0.3
        help_text.element.multiline = True
        help_text.element.wrap_lines = True
        help_text.position = w / 2., h / 2. + 300
        self.add(help_text)

        # tower information
        self.damage_pic = resources.picto_damage
        self.rate_pic = resources.picto_rate
        pic_width = resources.tower[1][1]["image"].width

        self.menuMin_x = (w / 2. - pic_width * (4 / 3) - 55)
        self.menuMin_y = 700

        towername_font = {
            'bold': True,
            'anchor_x': "right",
            'anchor_y': 'center',
            'font_size': 18,
            'color': (193, 249, 255, 255)
        }
        caption_font = {
            'bold': True,
            'anchor_x': "left",
            'anchor_y': 'center',
            'font_size': 15,
        }

        towername_label = []
        towername_label.append(text.Label("Rapidfire Tower", **towername_font))
        towername_label.append(text.Label("Range Tower", **towername_font))
        towername_label.append(text.Label("Plasma Tower", **towername_font))
        towername_label.append(text.Label("Poison Tower", **towername_font))
        towername_label.append(text.Label("Slow Tower", **towername_font))

        for j, m in enumerate(towername_label):
            m.position = (self.menuMin_x - 80, self.menuMin_y -
                          j * (pic_width + 15))

        try:
            for j in range(nr_towers):
                self.add(towername_label[j])
        except IndexError:
            print("please add towername_label for all towers. " +
                  "otherwise no labels will be printed")

        price_label = text.Label("$  Price",
                                 color=(255, 0, 0, 255), **caption_font)
        dam_pic = cocos.sprite.Sprite(self.damage_pic)
        dam_label = text.Label("Damage per hit",
                               color=(255, 70, 0, 255), **caption_font)
        rate_pic = cocos.sprite.Sprite(self.rate_pic)
        rate_label = text.Label("Firerate",
                                color=(0, 124, 244, 255), **caption_font)

        price_label.position = (self.menuMin_x - 30,
                                self.menuMin_y - (nr_towers * (pic_width + 15)))
        dam_pic.position = (self.menuMin_x + 103,
                            self.menuMin_y - (nr_towers * (pic_width + 15)))
        dam_label.position = (self.menuMin_x + 135,
                              self.menuMin_y - (nr_towers * (pic_width + 15)))
        rate_pic.position = (self.menuMin_x + 370,
                             self.menuMin_y - (nr_towers * (pic_width + 15)))
        rate_label.position = (self.menuMin_x + 402,
                               self.menuMin_y - (nr_towers * (pic_width + 15)))

        self.add(price_label)
        self.add(dam_pic)
        self.add(dam_label)
        self.add(rate_pic)
        self.add(rate_label)

        for l in range(1, 4):  # loop over upgrade levels
            self.towerDamagePic = []
            self.towerFireratePic = []
            self.towerThumbnails = []
            # loop over all tower thumbnails
            try:
                for i in range(nr_towers):
                    self.towerThumbnails.append(cocos.sprite.Sprite(
                        resources.tower[i][l]["image"]))
            except KeyError:
                print("check your tower naming, first tower should start " +
                      "with 0 and no number should be left out.")
                nr_towers = 0
            text_font = {
                'bold': True,
                'anchor_x': "left",
                'anchor_y': 'center',
                'font_size': 15,
                'color': (255, 70, 0, 255)
            }
            damage_label = []
            for i in range(nr_towers):
                damage_label.append(text.Label(" ", **text_font))
            self.towerDamageTexts = [n for n in damage_label]

            text_font['color'] = (0, 124, 244, 255)
            firerate_label = []
            for i in range(nr_towers):
                firerate_label.append(text.Label(" ", **text_font))
            self.towerFirerateTexts = [n for n in firerate_label]

            text_font['color'] = (255, 0, 0, 255)
            cost_label = []
            for i in range(nr_towers):
                cost_label.append(text.Label(" ", **text_font))
            self.towerCostTexts = [n for n in cost_label]

            for picture in range(nr_towers):
                self.towerThumbnails[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100),
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y)

                self.towerDamagePic.append(
                    cocos.sprite.Sprite(self.damage_pic))
                self.towerDamagePic[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 15,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y)

                self.towerDamageTexts[picture].element.text = (
                    str(resources.tower[picture][l]["damage"]))
                self.towerDamageTexts[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 35,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y)

                self.towerFireratePic.append(
                    cocos.sprite.Sprite(self.rate_pic))
                self.towerFireratePic[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 15,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y - 25)

                self.towerFirerateTexts[picture].element.text = (
                    str(resources.tower[picture][l]["firerate"]))
                self.towerFirerateTexts[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 35,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y - 25)

                self.towerCostTexts[picture].element.text = (
                        '$ ' + str(resources.tower[picture][l]["cost"]))
                self.towerCostTexts[picture].position = (
                    self.menuMin_x +
                    (l - 1) * (self.towerThumbnails[picture].width + 100) +
                    self.towerThumbnails[picture].width / 2. + 15,
                    -picture * (self.towerThumbnails[picture].width + 15) +
                    self.menuMin_y + 25)

                self.add(self.towerThumbnails[picture])
                self.add(self.towerDamageTexts[picture])
                self.add(self.towerFirerateTexts[picture])
                self.add(self.towerDamagePic[picture])
                self.add(self.towerFireratePic[picture])
                self.add(self.towerCostTexts[picture])

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True


class AboutLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0, 0, 0, 1, width=w, height=h - 86)

    def on_enter(self):
        super().on_enter()
        w, h = director.get_window_size()

        about_text = text.Label('PyFense ist ein Tower Defense Spiel ' +
                                'welches im Rahmen des Python ' +
                                'Projektpraktikums an der TU ' +
                                'München von fünf Studenten programmiert ' +
                                'wurde.\nMitglieder: Daniel, Jakob, ' +
                                'Matthias, Nimar, Robin' +
                                '\nMusic from:\n' +
                                'www.freesound.org/people/djgriffin/',
                                font_name=_font_,
                                font_size=20,
                                anchor_x='center',
                                anchor_y='center')
        about_text.element.width = w * 0.3
        about_text.element.multiline = True
        about_text.element.wrap_lines = True
        about_text.position = w / 2., h / 2.
        self.add(about_text)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True


def end_run():
    current_wave = director.interpreter_locals["current_wave"]
    earned = director.interpreter_locals["earned"]
    lives_left = director.interpreter_locals["lives_left"]
    spent = director.interpreter_locals["spent"]

    director.window.close()
    collect()  # garbage collection to avoid pyglet runtime error (hopefully)

    return [current_wave, lives_left, spent, earned]


def init_director():
    director.init(**resources.settings['window'])
    director.window.set_vsync(True)
    director.window.set_fullscreen(False, None, None, 640, 360)

    # if SCREEN == 1:
    #     # full screen:
    #     director.window.set_fullscreen(fullscreen=True)
    # elif SCREEN == 2:
    #     # small screen:
    #     director.window.set_fullscreen(False, None, None, 640, 360)


def run_single_game(genome, waves_number,lives_left, init_wave, gen_num=0):
    # making sure game would start *exactly* on wave specified by user, and not +1
    init_wave = init_wave - 1 if init_wave > 0 else 0
    
    init_director()
    director.run(game.PyFenseGame(genome, waves_number, lives_left, init_wave=init_wave, gen_num=gen_num))

    return end_run()


def run_sequence_of_genomes(genomes, waves_number):
    init_director()

    director.run(game.PyFenseGame(genomes, waves_number))

    return end_run()


def display_genome_from_string(string_genome):

    genomes = [decode_genome_from_string(string_genome)]

    init_director()

    director.run(game.PyFenseGame(genomes, gen_num=-1))

    end_run()

def decode_genome_from_string(string_genome):
    genome = []
    tower_encodings_list = string_genome.split()
    for item in tower_encodings_list:
        new_tower = Tower()

        type_int = -1 if item[0] == '-' else int(item[0])

        if type_int > 0:
            new_tower.update(TowerType(type_int), TowerLevel(int(item[1])))

        genome.append(new_tower)

    return np.array(genome)

def run_genomes(genome_dict, output_dict, init_wave, waves_number, generation):

    # run all individuals
    runs = 1
    for key in genome_dict.keys():
        value = genome_dict[key]
        genome = decode_genome_from_string(value[0])
        lives_left = int(value[1])
        # print("Run genome: " + str(runs) + " Generation: " + str(generation) + " Segment: " + str(init_wave // 9) +
        #       " Initial life: " + str(lives_left))
        values = run_single_game([genome], waves_number, lives_left, init_wave=init_wave, gen_num=generation)
        output_dict[key] = values
        # print("     wave = " + str(values[0]) +
        #       " lives = " + str(values[1]) +
        #       " money_spent = " + str(values[2]) +
        #       " money_earned = " + str(values[3])
        #       )
        runs += 1

def create_genomes_dict_from_csv(path):
    """
    Create a dictionary of genomes from csv file path
    """
    with open(path) as f:
        genome_dict = json.load(f)
    return genome_dict
        

def write_dict(path, dictionary):
    """
    write dictionary to path file
    """
    with open(path, 'w') as f:
        json.dump(dictionary, f)


# def create_flag(flag_path):
#     """
#     Create flag file according to path
#     """
#     os.mkdir(flag_path)


def run_generation():
    """
    run genomes for generation
    """
    input_csv_path = sys.argv[2]
    outut_csv_path = sys.argv[3]
    init_wave = int(sys.argv[4])
    num_waves = int(sys.argv[5])
    generation = int(sys.argv[6])

    genome_dict = create_genomes_dict_from_csv(input_csv_path)
    output_dict = dict()
    run_genomes(genome_dict, output_dict, init_wave, num_waves, generation)
    write_dict(outut_csv_path, output_dict)


def run_solution():
    """
    Run a given solution
    """
    input_json_path = sys.argv[2]
    output_path = sys.argv[3]
    num_waves = int(sys.argv[4])
    sols_dict = create_genomes_dict_from_csv(input_json_path)
    data = dict()

    for seg_id in range(len(sols_dict)):

        seg_sol = list()

        for genome in sols_dict[str(seg_id)]:
            seg_sol.append(decode_genome_from_string(genome))

        print("Sol for seg " + str(seg_id))
        data[seg_id] = run_sequence_of_genomes(seg_sol, num_waves)

    with open(output_path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    mode = sys.argv[1]

    if mode == "learn":
        run_generation()

    else:  # mode is "solution"
        run_solution()
