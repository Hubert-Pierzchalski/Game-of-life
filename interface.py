import arcade
from scipy import signal
import numpy as np
import math
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel
from arcade.gui.events import UIOnChangeEvent
import logic

class PreGame(arcade.Window):

    def __init__(self, width, height, randomizer: bool, ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, MARGIN):
        super().__init__(width, height, randomizer)

        self.ROW_COUNT = ROW_COUNT
        self.COLUMN_COUNT = COLUMN_COUNT
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.MARGIN = MARGIN
        self.randomizer = randomizer

        self.real_value = 1/5
        self.set_update_rate(1 / 5)
        self.updating = False
        self.random()
        self.background_color = arcade.color.BLACK
        self.grid_sprite_list = arcade.SpriteList()
        self.manager = UIManager()
        self.manager.enable()

        refresh_rate = UISlider(value=35, width=300, height=50)
        label = UILabel(text=f"updates per second {5:02.0f}")

        @refresh_rate.event()

        def on_change(event: UIOnChangeEvent):
            self.real_value = 2/(refresh_rate.value+1)
            show_value = 1/self.real_value
            label.text = f"Updates per second :{show_value:02.0f}"
            self.set_update_rate(self.real_value)
            label.fit_content()

        self.manager.add(UIAnchorWidget(child=refresh_rate, anchor_x='left', anchor_y='bottom', align_y=0, align_x=0))
        self.manager.add(UIAnchorWidget(child=label, anchor_x='left', anchor_y='bottom', align_y=50, align_x=75))

        width, height = self.get_size()
        logic.adjust_to_screen(WIDTH, HEIGHT, MARGIN)

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN + 75)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_y = y
                sprite.center_x = x
                self.grid_sprite_list.append(sprite)

        self.resync_grid_with_sprites()

    def random(self):

        if self.randomizer:
            self.grid = np.array(np.random.randint(2, size=(self.ROW_COUNT, self.COLUMN_COUNT)))
        else:
            self.grid = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def on_draw(self):

        self.clear()

        self.grid_sprite_list.draw()
        self.manager.draw()

    def resync_grid_with_sprites(self):
        for row in range(self.ROW_COUNT):
            for column in range(self.COLUMN_COUNT):
                pos = row * self.COLUMN_COUNT + column
                if self.grid[row][column] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                else:
                    self.grid_sprite_list[pos].color = arcade.color.BLACK

    def on_mouse_press(self, x, y, button, modifiers):

        column = int(x // (self.WIDTH + self.MARGIN))
        if y >= 75:
            row = int((y-75) // (self.HEIGHT + self.MARGIN))

        if row >= self.ROW_COUNT or column >= self.COLUMN_COUNT:
            return

        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0

        self.resync_grid_with_sprites()


    def on_update(self, delta_time: float):

        if self.updating:
            self.grid = logic.check_grid(self.grid)
            self.resync_grid_with_sprites()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:
            if self.updating:
                self.updating = False
            else:
                self.updating = True

        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            print(width, height)
            self.set_viewport(0, width, 0, height)

        if key == arcade.key.R:

            self.updating = False
            self.random()
            self.resync_grid_with_sprites()

        if key == arcade.key.L:
            if self.randomizer:
                self.randomizer = False
            else:
                self.randomizer = True

        if key == arcade.key.ESCAPE:
            arcade.exit()

        if key == arcade.key.KEY_1:
            self.grid = logic.read_pattern("glider")

        if key == arcade.key.KEY_2:
            self.grid = logic.read_pattern("gosper-glider-gun")

        if key == arcade.key.KEY_3:
            self.grid = logic.read_pattern("pulsar")

        if key == arcade.key.RIGHT:
            self.updating = True
            self.on_update(self.real_value)
            self.updating = False
