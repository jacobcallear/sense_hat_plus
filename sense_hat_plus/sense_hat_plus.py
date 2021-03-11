from time import sleep

from sense_hat import SenseHat

from sense_hat_plus.snake_hat import GameOver, SnakeGame


class SenseHatPlus(SenseHat):
    '''Raspberry Pi Sense HAT with extra powers.

    Initiate with:
    >>> s = SenseHatPlus()
    '''

    def __init__(self):
        super().__init__()
        self.snake_game = SnakeGame()

    def play_snake(self, time_interval=0.5):
        """Play the snake game with the joystick and an LED grid!

        Example:
        >>> sense_hat = SenseHatPlus()
        >>> sense_hat.play_snake()
        """
        SNAKE_COLOUR = (255, 0, 0)
        FOOD_COLOUR = (255, 255, 255)
        BLANK_COLOUR = (0, 0, 0)

        # Set up board
        self.snake_game = SnakeGame()
        self.clear()
        x, y = self.snake_game.snake[0]
        self.set_pixel(x, y, SNAKE_COLOUR)

        # Wait for player to move joystick
        self.stick.get_events()  # Clear previous joystick movements
        print('Move joystick to continue')
        while True:
            try:
                direction = self.stick.get_events()[-1].direction
                break
            except IndexError:
                sleep(time_interval)

        # Start game!
        while True:
            # Add food pixel
            if not self.snake_game.is_food_on_board:
                # If no space to add food, you've won!
                try:
                    self.snake_game.add_food()
                except GameOver:
                    self.show_snake_game_over()
                    break
                x, y = self.snake_game.food_coordinate
                self.set_pixel(x, y, FOOD_COLOUR)

            # Get direction to move snake
            sleep(time_interval)
            try:
                direction = self.stick.get_events()[-1].direction
            except IndexError:
                pass

            # Add pixel to snake head IF valid move
            try:
                x, y = self.snake_game.move_snake(direction)
            except GameOver:
                self.show_snake_game_over()
                break
            self.set_pixel(x, y, SNAKE_COLOUR)

            # Remove pixel from snake tail UNLESS it has just eaten food
            coordinate_to_remove = self.snake_game.pop_from_tail()
            if coordinate_to_remove:
                x, y = coordinate_to_remove
                self.set_pixel(x, y, BLANK_COLOUR)

    def show_snake_game_over(self):
        '''Show snake game-over text.'''
        self.clear(255, 255, 255)
        sleep(2)
        score = len(self.snake_game.snake)
        if score == 64:
            self.show_message('! ' * 5, back_colour=(75, 0, 0))
        self.show_message(str(score))
        print(score)
        sleep(1)
        self.clear()
