import pygame as pg
from collections import namedtuple

Grid = namedtuple('Grid', ['width', 'height'])
Rect = namedtuple('Dimensions', ['width', 'height'])

class Game():
    """Game class to display ASCII art with colors."""
    def __init__(
        self,
        screen_resolution: tuple[int, int] = (1920, 1080),
        num_chars_width: int = 192,
        font_relative_file_path: str="fonts/Roboto_Mono/static/RobotoMono-Bold.ttf",
    ) -> None:
        """
        Displays a list of strings as an image in a Pygame window.

        Args:
            ascii_image (list of str): The list of strings to display.
            rgb_data (list of tuples): A list of RGB tuples corresponding to the pixels.
            window_size (tuple): The size of the Pygame window (width, height).
            font_size (int): The font size of the characters.
        """
        # Initialize Pygame
        pg.init()

        # Initialisations
        self.background_color = (0, 0, 0)
        self.font_relative_file_path = font_relative_file_path
        self.screen_resolution = Rect(screen_resolution[0], screen_resolution[1])
        self.num_chars_width = num_chars_width

        # Computations
        self.font_ratio = self.compute_average_font_ratio()
        self.font_size, self.font_resolution = self.compute_font_dimensions()
        self.num_chars = self.compute_num_chars_dimensions()
        self.num_chars_height = self.num_chars.height

        # Settings.
        self.font = pg.font.Font(self.font_relative_file_path, self.font_size)
    
    def compute_num_chars_dimensions(
        self,
    ) -> int:
        """ """
        num_chars_height = int(self.screen_resolution.height / self.font_resolution.height)
        return Rect(self.num_chars_width, num_chars_height)
    
    def compute_font_dimensions(
        self,
        test_char: str = 'A',
        height_empirical_adjust_ratio: float=0.56
    ) -> tuple[int, tuple[int, int]]:
        """ """
        target_width = self.screen_resolution.width / self.num_chars_width
        font_size = 1

        while True:
            font = pg.font.Font(self.font_relative_file_path, font_size)
            width, height = font.size(test_char)
            if width >= target_width:
                break
            font_size += 1

        height *= height_empirical_adjust_ratio
        font_resolution = Rect(width, int(height))

        return font_size, font_resolution

    def compute_average_font_ratio(
        self,
        test_font_size: int=72,
    ) -> float:
        """ """
        font = pg.font.Font(self.font_relative_file_path, test_font_size)
        test_chars = "ABCDEFGHIJKLMNOPQURSTUVWXYZ!@#$%^&*()-_=+[]\|;:'/?.>,<~`"

        avg_width, avg_height = [
            sum(dim) / len(test_chars) for dim in zip(
                *[font.size(char) for char in test_chars]
            )
        ]
        
        return avg_height / avg_width
    
    def draw_tiles(
        self,
        screen,
        y: int,
        x: int,
        tile: tuple,
        tile_size: int,
        color_mapping: dict
    ):
        """ """

        for set_index, cell in enumerate(list(tile)):
            x_cell, y_cell = set_index % tile_size, set_index // tile_size
            color = color_mapping[cell]
            text_surface = self.font.render(cell, True, color)
            screen.blit(text_surface,
                (
                    tile_size * x * self.font_resolution.width + x_cell * self.font_resolution.width,
                    tile_size * y * self.font_resolution.height + y_cell * self.font_resolution.height
                )
            )
    
    def start_game(
        self,
        pattern,
        color_mapping,
        tile_size,
    ) -> None:
        """ """
        screen = pg.display.set_mode(
            (self.screen_resolution.width, self.screen_resolution.height)
        )
        pg.display.set_caption("ASCII Art with Colors")

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            screen.fill(self.background_color)

            for y, line in enumerate(pattern):
                for x, tile in enumerate(line):
                    self.draw_tiles(screen, y, x, tile, tile_size, color_mapping)

            pg.display.flip()

        # Quit Pygame 
        pg.quit()