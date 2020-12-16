from collections import deque
from random import randint

from sense_hat import SenseHat


class GameOver(Exception):
    '''Raised when snake game is lost.'''
    pass


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
        self.set_pixel(random_coord[0], random_coord[1], (255, 0, 0))
        self.free_coords.remove(random_coord)

    def advance(self, direction):
        '''Add pixel to head of snake in given direction.'''
        x, y = self.snake[-1]
        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        # End game if hit edge of board
        for coord in (x, y):
            if coord < 0 or coord > 7:
                raise GameOver(f'Hit edge of board (x={x}, y={y})')
        # Advance snake head
        self.snake.append((x, y))
        self.set_pixel(x, y, (255, 0, 0))
        self.free_coords.remove((x, y))
        # Remove snake tail
        tail = self.snake.popleft()
        self.set_pixel(tail[0], tail[1], (0, 0, 0))
        self.free_coords.add(tail)
