import interface
import arcade
import logic


def main():
    ROW_COUNT = 30
    COLUMN_COUNT = 100
    WIDTH = 14
    HEIGHT = 14
    MARGIN = 5
    SCREEN_WIDTH, SCREEN_HEIGHT = logic.matrix_dimensions(ROW_COUNT, COLUMN_COUNT, HEIGHT, WIDTH, MARGIN)
    randomizer = False
    interface.PreGame(SCREEN_WIDTH, SCREEN_HEIGHT, randomizer, ROW_COUNT, COLUMN_COUNT, WIDTH, HEIGHT, MARGIN)
    arcade.run()


if __name__ == "__main__":
    main()