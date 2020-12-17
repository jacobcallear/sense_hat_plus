from collections import deque
from random import randint, sample
from time import sleep

from sense_hat import SenseHat


class GameOver(Exception):
    '''Raised when snake game is finished.'''
    pass


class SnakeHat(SenseHat):
    '''Describes the 8x8 LED grid for a snake game.'''

    opposite_directions = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }

    def __init__(self):
        '''Connect to SenseHat and create snake with one pixel.'''
        super().__init__()
        # Light pixels
        self.clear()
        snake_pixel = (randint(0, 7), randint(0, 7))
        self.set_pixel(snake_pixel[0], snake_pixel[1], (255, 0, 0))
        # Describe position of snake on LED grid
        self.snake = deque([snake_pixel])
        self.free_coords = {
            (x, y)
            for x in range(8)
            for y in range(8)
        }
        self.food_on_board = False
        self.food_coord = None

    def move_snake(self, direction):
        '''Move snake in given direction and add food pixel.'''
        # Add food if needed
        self.__add_food()
        coord_to_add = self.__get_next_coord(direction)
        self.__check_valid_coord(coord_to_add)
        self.__add_to_head(coord_to_add)
        self.__pop_from_tail()

    def __get_next_coord(self, direction):
        '''Return head of snake shifted one pixel in `direction`.'''
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
        coord_to_add = (x, y)
        # If try to turn immediately back into themselves, keep previous direction
        if len(self.snake) != 1 and self.snake[-2] == coord_to_add:
            return self.__get_next_coord(self.opposite_directions[direction])
        return coord_to_add

    def __check_valid_coord(self, coord):
        '''Raise GameOver exception if snake hit edges or itself.'''
        # End game if hit body
        if coord not in self.free_coords:
            raise GameOver('Hit yourself')
        # End game if hit edge of board
        for x_or_y in coord:
            if not 0 <= x_or_y <= 7:
                x, y = coord
                raise GameOver(f'Hit edge of board (x={x}, y={y})')

    def __add_to_head(self, coord_to_add):
        '''Add given coordinate to snake.'''
        self.snake.append(coord_to_add)
        self.set_pixel(coord_to_add[0], coord_to_add[1], (255, 0, 0))
        self.free_coords.remove(coord_to_add)

    def __pop_from_tail(self):
        '''Check if eaten food; if not, remove last pixel from snake.'''
        # Remove snake tail if not eaten food
        head_coord = self.snake[-1]
        if head_coord != self.food_coord:
            tail = self.snake.popleft()
            self.set_pixel(tail[0], tail[1], (0, 0, 0))
            self.free_coords.add(tail)
        else:
            self.food_on_board = False

    def __add_food(self):
        '''Add food pixel to board if food not already on board.'''
        if not self.food_on_board:
            # End game if snake fills whole board
            if self.free_coords == set():
                raise GameOver('You won!')
            # Choice random coordinate for food
            self.food_coord = sample(self.free_coords, 1)[0]
            x, y = self.food_coord
            self.set_pixel(x, y, (255, 255, 255))
            self.food_on_board = True

    def show_game_over(self):
        '''Show game over text.'''
        self.clear(255, 255, 255)
        sleep(2)
        score = len(self.snake)
        if score == 64:
            self.show_message('! ' * 5, back_colour=(75, 0, 0))
        self.show_message(str(score))
        print(score)
        sleep(1)
        self.clear()
