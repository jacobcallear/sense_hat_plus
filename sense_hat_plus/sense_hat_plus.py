from time import sleep

from sense_hat import SenseHat

from sense_hat_plus.snake_hat import GameOver, SnakeHat


class SenseHatPlus(SenseHat):
    '''Raspberry Pi Sense HAT with extra powers.

    Initiate with:
    >>> s = SenseHatPlus()
    '''

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
            # Get direction
            try:
                direction = snake_hat.stick.get_events()[-1].direction
            except IndexError:
                pass
            # Move snake
            try:
                snake_hat.move_snake(direction)
            except GameOver:
                snake_hat.show_game_over()
                break
