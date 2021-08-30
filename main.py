import arcade
from PIL import Image
import random

#constants for screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

cactus = Image.open("images\cactus.png")

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BEIGE)
    
    def setup(self):
        """" Set up game and initialize the variables """

        # Create sprite lists
        self.player_list = arcade.SpriteList
        self.coin_list = arcade.SpriteList

        SPRITE_SCALING_COIN = 0.2
        SPRITE_SCALING_PLAYER = 1.0
        COIN_COUNT = 10
        coin = arcade.Sprite("images/coin.png", SPRITE_SCALING_COIN)

        # Score
        self.score = 0

        # Set up the player
        self.player_sprite = arcade.Sprite("images/cactus.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50 # Starting position
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            coin = arcade.Sprite("images/coin.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)


    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Draw everything
        self.coin_list.draw()
        self.player_list.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # Generate a list of all coin sprites that collided with the player.  
        coins_hit_list = (arcade.check_for_collision_with_list(self.player_sprite, arcade.SpriteList(self.coin_list)))

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.kill()
            self.score += 1


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()
