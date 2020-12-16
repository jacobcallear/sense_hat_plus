from collections import deque
from random import randint

from sense_hat import SenseHat


class SnakeHat(SenseHat):
    '''Describes the 8x8 LED grid for a snake game.'''
    
    opposite_directions = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        random_coord = tuple(randint(0, 7) for _ in range(2))
        # Describe position of snake on LED grid
        self.snake = deque([random_coord])
        self.free_coords = {
            (x, y)
            for x in range(8)
            for y in range(8)
        }
        # Light pixels on board
        self.clear()
        self.set_pixel(random_coord, (255, 0, 0))
        free_coords.remove(random_coord)
