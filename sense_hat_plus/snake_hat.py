from collections import deque
from random import randint

from sense_hat import SenseHat


class GameOver(Exception):
    '''Raised when snake game is lost.'''
    pass


class SnakeHat(SenseHat):
    '''Describes the 8x8 LED grid for a snake game.'''

    def __init__(self):
        super().__init__()
        # Light pixels
        self.clear()
        snake_pixel = self.set_random_pixel(colour=(255, 0, 0))
        # Describe position of snake on LED grid
        self.snake = deque([snake_pixel])
        self.snake_set = set(self.snake)
        self.need_food = True

    def advance(self, direction):
        '''Add pixel to head of snake in given direction.'''
        # Add food if needed
        self.add_food()
        # Determine new coordinate
        x, y = self.snake[-1]
        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        # End game if hit body
        coord_to_add = (x, y)
        if coord_to_add in self.snake_set:
            raise GameOver('Hit yourself')
        # End game if hit edge of board
        for coord in coord_to_add:
            if coord < 0 or coord > 7:
                raise GameOver(f'Hit edge of board (x={x}, y={y})')
        # End game if snake fills all board
        if len(self.snake) == 64:
            raise GameOver('You won!')
        # Advance snake head
        self.snake.append(coord_to_add)
        self.set_pixel(x, y, (255, 0, 0))
        self.snake_set.add(coord_to_add)
        # Remove snake tail if not eaten food
        if coord_to_add != self.food_coord:
            tail = self.snake.popleft()
            self.set_pixel(tail[0], tail[1], (0, 0, 0))
            self.snake_set.remove(tail)
        else:
            self.need_food = True

    def add_food(self):
        if self.need_food:
            self.food_coord = self.set_random_pixel(colour=(255, 255, 255))

    def set_random_pixel(self, colour=(255, 255, 255)):
        '''Set random pixel to given colour and return (x, y) coordinates.'''
        random_pixel = (randint(0, 7), randint(0, 7))
        self.set_pixel(randint(0, 7), randint(0, 7), colour)
        return random_pixel
