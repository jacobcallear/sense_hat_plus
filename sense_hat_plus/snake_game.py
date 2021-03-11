'''Defines SnakeGame class to use in SenseHatPlus class.'''
from collections import deque
from random import randint, sample


class GameOver(Exception):
    '''Raised when snake game is finished.'''
    pass


class SnakeGame():
    '''Describes a snake game on an 8x8 coordinate system.

    Attributes:
        snake (collections.deque): List of coordinates that make up the snake
            The head of the snake is at index -1. Each coordinate is in the
            form `(x, y)`, where x and y are integers between 0 and 7
            (inclusive).
        free_coordinates (set): Set of empty coordinates (i.e. not part of the
            snake or food).
        food_coordinate (tuple[int]): (x, y) coordinate of food item.
        is_food_on_board (bool): True if food is on the board (i.e.
            self.food_coordinate is not in self.free_coordinates); otherwise
            False.
    '''

    _opposite_directions = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }

    def __init__(self):
        '''Initialises snake game with a one pixel snake at a random
        coordinate.'''
        # Describe position of snake on LED grid
        snake_coordinate = (randint(0, 7), randint(0, 7))
        self.snake = deque([snake_coordinate])
        self.free_coordinates = {
            (x, y)
            for x in range(8)
            for y in range(8)
        }
        self.food_coordinate = ()
        self.is_food_on_board = False

    def move_snake(self, direction):
        '''Moves snake in given direction.

        Raises:
            GameOver: If you try to move the snake to a coordinate that is not
                in `self.free_coordinates`.

        Figures out coordinate if snake moves one pixel in `direction`. Adds
        this coordinate to `self.snake`, and removes it from
        `self.free_coordinates`.
        '''
        next_coordinate = self._get_next_coordinate(direction)
        self._check_valid_coordinate(next_coordinate)
        self.snake.append(next_coordinate)
        self.free_coordinates.remove(next_coordinate)
        return next_coordinate

    def pop_from_tail(self):
        '''Check if eaten food; if not, remove last pixel from snake.

        If snake has just eaten food, does nothing and returns empty tuple.
        Otherwise, removes last coordinate from snake and returns it, and adds
        this coordinate to `self.free_coordinates`
        '''
        # Remove snake tail if not eaten food
        head_coord = self.snake[-1]
        if head_coord != self.food_coordinate:
            tail = self.snake.popleft()
            self.free_coordinates.add(tail)
            return tail
        self.is_food_on_board = False
        return ()

    def add_food(self):
        '''Chooses random free coordinate to convert to food.

        Raises:
            GameOver: If there is no space left on the board (i.e. you won the
                game).

        Before calling this method, check that `self.is_food_on_board` is
        False.
        '''
        # End game if snake fills whole board
        if self.free_coordinates == set():
            raise GameOver('You won!')
        # Choose random coordinate for food
        self.food_coordinate = sample(self.free_coordinates, 1)[0]
        self.is_food_on_board = True

    def _get_next_coordinate(self, direction):
        '''Return head of snake shifted one pixel in `direction`.

        Called by `self.move_snake()`
        '''
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
        next_coordinate = (x, y)
        # Keep previous direction if they try to do an immediate about turn
        if len(self.snake) != 1 and self.snake[-2] == next_coordinate:
            opposite_direction = self._opposite_directions[direction]
            return self._get_next_coordinate(opposite_direction)
        return next_coordinate

    def _check_valid_coordinate(self, coordinate):
        '''Raise GameOver exception if snake hit edges or itself.

        Called by `self.move_snake()`
        '''
        # End game if hit body
        if coordinate not in self.free_coordinates:
            raise GameOver('Hit yourself')
        # End game if hit edge of board
        for x_or_y in coordinate:
            if not 0 <= x_or_y <= 7:
                x, y = coordinate
                raise GameOver(f'Hit edge of board (x={x}, y={y})')
