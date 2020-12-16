from time import sleep

from sense_hat import SenseHat

from sense_hat_plus.snake_hat import GameOver, SnakeHat


class SenseHatPlus(SenseHat):
    '''Raspberry Pi Sense HAT with extra powers.

    Initiate with:
    >>> s = SenseHatPlus()
    '''

    opposite_directions = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }

    def play_snake(self, time_interval=0.5):
        # Start game and clear previous joystick movemetns
        snake_hat = SnakeHat()
        snake_hat.stick.get_events()
        # Start game when joystick moved
        print('Move joystick to continue')
        while True:
            try:
                event = snake_hat.stick.get_events()[-1]
            except IndexError:
                sleep(time_interval)
            else:
                direction = event.direction
                break
        # Move snake when joystick moved
        while True:
            sleep(time_interval)
            try:
                event = snake_hat.stick.get_events()[-1]
            except IndexError:
                pass
            else:
                # If snake turns directly back into itself, keep going in the
                # previous direction
                # i.e. if snake '====>' turns '<-', keep moving '->' instead of
                # ending game
                next_direction = event.direction
                turning_back = next_direction == self.opposite_directions[direction]
                if not turning_back or len(snake_hat.snake) == 1:
                    direction = next_direction
            # Move snake
            try:
                snake_hat.advance(direction)
            except GameOver:
                snake_hat.show_game_over()
                break
